import boto3
import json
import os
import time
import urllib.request
import urllib.error

dynamodb = boto3.resource('dynamodb')
history_table = dynamodb.Table(os.environ['TABLE_NAME'])
kb_table = dynamodb.Table(os.environ['KB_TABLE_NAME'])
orders_table = dynamodb.Table(os.environ['ORDERS_TABLE'])

bedrock = boto3.client('bedrock-runtime')
cloudwatch = boto3.client('cloudwatch')

MODEL_ID = os.environ['MODEL_ID']
EMBED_MODEL_ID = os.environ['EMBED_MODEL_ID']

# Nova Micro pricing (USD per token) - used only for rough cost logging
INPUT_COST_PER_TOKEN = 0.035 / 1_000_000
OUTPUT_COST_PER_TOKEN = 0.14 / 1_000_000

SYSTEM_PROMPT = [{
    "text": (
        "You are a helpful customer support assistant for an online store called CloudCart. "
        "You can check order status, search CloudCart's internal help documents, and check "
        "the weather (useful for shipping-delay questions). Use the available tools whenever "
        "they would help answer the user's question, rather than guessing. Keep answers concise "
        "and friendly."
    )
}]

TOOLS = [
    {
        "toolSpec": {
            "name": "check_order_status",
            "description": "Look up the current status of a customer's order using its order ID.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "The order ID, e.g. ORD-1001"}
                    },
                    "required": ["order_id"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "search_knowledge_base",
            "description": "Search CloudCart's internal help documents (shipping, returns, warranty policies, etc.) for information relevant to the user's question.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "What to search for"}
                    },
                    "required": ["query"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "get_weather",
            "description": "Get current weather conditions for a location, given its latitude and longitude. Useful for answering questions about possible shipping delays.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"}
                    },
                    "required": ["latitude", "longitude"]
                }
            }
        }
    }
]


def handler(event, context):
    start_time = time.time()
    try:
        body = json.loads(event.get('body') or '{}')
        session_id = body.get('session_id', 'default')
        user_message = body.get('message', '')

        if not user_message:
            return response(400, {"error": "message is required"})

        item = history_table.get_item(Key={'session_id': session_id}).get('Item')
        history = item['history'] if item else []
        history.append({"role": "user", "content": [{"text": user_message}]})

        total_input_tokens = 0
        total_output_tokens = 0
        output_message = None

        # Agent loop: the model may call tools multiple times before answering.
        # Cap iterations so a misbehaving tool loop can't run forever.
        for _ in range(4):
            result = bedrock.converse(
                modelId=MODEL_ID,
                messages=history,
                system=SYSTEM_PROMPT,
                inferenceConfig={"maxTokens": 512},
                toolConfig={"tools": TOOLS}
            )

            usage = result.get("usage", {})
            total_input_tokens += usage.get("inputTokens", 0)
            total_output_tokens += usage.get("outputTokens", 0)

            output_message = result["output"]["message"]
            history.append(output_message)

            if result.get("stopReason") == "tool_use":
                tool_results = []
                for block in output_message["content"]:
                    if "toolUse" in block:
                        tool_use = block["toolUse"]
                        tool_output = execute_tool(tool_use["name"], tool_use.get("input", {}))
                        tool_results.append({
                            "toolResult": {
                                "toolUseId": tool_use["toolUseId"],
                                "content": [{"json": tool_output}]
                            }
                        })
                history.append({"role": "user", "content": tool_results})
                continue
            else:
                break

        assistant_reply = "".join(
            block["text"] for block in output_message["content"] if "text" in block
        )

        history_table.put_item(Item={
            'session_id': session_id,
            'history': history[-20:],
            'updated_at': int(time.time())
        })

        latency_ms = int((time.time() - start_time) * 1000)
        log_metrics(latency_ms, total_input_tokens, total_output_tokens)

        return response(200, {"reply": assistant_reply})

    except Exception as e:
        return response(500, {"error": str(e)})


def execute_tool(name, tool_input):
    try:
        if name == "check_order_status":
            return check_order_status(tool_input.get("order_id", ""))
        elif name == "search_knowledge_base":
            return search_knowledge_base(tool_input.get("query", ""))
        elif name == "get_weather":
            return get_weather(tool_input.get("latitude"), tool_input.get("longitude"))
        else:
            return {"error": f"Unknown tool: {name}"}
    except Exception as e:
        return {"error": str(e)}


def check_order_status(order_id):
    resp = orders_table.get_item(Key={"order_id": order_id})
    item = resp.get("Item")
    if not item:
        return {"error": f"No order found with ID {order_id}"}
    return {
        "order_id": order_id,
        "status": item.get("status"),
        "item": item.get("item")
    }


def search_knowledge_base(query):
    query_vector = embed_text(query)

    # Small demo knowledge base - scanning all chunks and scoring in
    # Lambda is fine here. A production system would use a real vector
    # store (e.g. OpenSearch or Bedrock Knowledge Bases) instead.
    items = kb_table.scan().get("Items", [])

    scored = []
    for it in items:
        vector = [float(x) for x in it["vector"]]
        score = cosine_similarity(query_vector, vector)
        scored.append((score, it["text"]))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    top_chunks = [text for _, text in scored[:3]]

    return {"results": top_chunks if top_chunks else ["No relevant documents found."]}


def get_weather(latitude, longitude):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
        current = data.get("current_weather", {})
        return {
            "temperature_c": current.get("temperature"),
            "windspeed_kmh": current.get("windspeed")
        }
    except urllib.error.URLError as e:
        return {"error": f"Could not fetch weather: {e}"}


def embed_text(text):
    resp = bedrock.invoke_model(
        modelId=EMBED_MODEL_ID,
        body=json.dumps({"inputText": text})
    )
    body = json.loads(resp["body"].read())
    return body["embedding"]


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def log_metrics(latency_ms, input_tokens, output_tokens):
    estimated_cost = (input_tokens * INPUT_COST_PER_TOKEN) + (output_tokens * OUTPUT_COST_PER_TOKEN)
    try:
        cloudwatch.put_metric_data(
            Namespace="CloudCartAgent",
            MetricData=[
                {"MetricName": "LatencyMs", "Value": latency_ms, "Unit": "Milliseconds"},
                {"MetricName": "InputTokens", "Value": input_tokens, "Unit": "Count"},
                {"MetricName": "OutputTokens", "Value": output_tokens, "Unit": "Count"},
                {"MetricName": "EstimatedCostUSD", "Value": estimated_cost, "Unit": "None"}
            ]
        )
    except Exception:
        # Never let metrics logging break the actual response
        pass


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }