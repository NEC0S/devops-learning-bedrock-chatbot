import boto3
import json
import os
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
bedrock = boto3.client('bedrock-runtime')
MODEL_ID = os.environ['MODEL_ID']


def handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        session_id = body.get('session_id', 'default')
        user_message = body.get('message', '')

        if not user_message:
            return response(400, {"error": "message is required"})

        # Load existing conversation history for this session
        item = table.get_item(Key={'session_id': session_id}).get('Item')
        history = item['history'] if item else []

        history.append({"role": "user", "content": user_message})

        # Call Bedrock using Anthropic's Messages API format
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "messages": history
        }

        result = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(payload)
        )

        result_body = json.loads(result['body'].read())
        assistant_reply = result_body['content'][0]['text']

        history.append({"role": "assistant", "content": assistant_reply})

        # Save updated history, keeping only the last 20 messages
        table.put_item(Item={
            'session_id': session_id,
            'history': history[-20:],
            'updated_at': int(time.time())
        })

        return response(200, {"reply": assistant_reply})

    except Exception as e:
        return response(500, {"error": str(e)})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }