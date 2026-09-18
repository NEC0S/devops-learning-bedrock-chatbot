"""
Chunks knowledge/docs.txt (one chunk per paragraph), embeds each chunk with
Amazon Titan Text Embeddings V2, and writes {chunk_id, text, vector} into the
knowledge base DynamoDB table. Safe to re-run: chunk IDs are stable, so
re-running just overwrites the same items.

Requires env vars: TABLE_NAME, AWS region configured via AWS CLI/credentials.
"""

import boto3
import json
import os
from decimal import Decimal

TABLE_NAME = os.environ["TABLE_NAME"]
EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"
DOCS_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge", "docs.txt")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
bedrock = boto3.client("bedrock-runtime")


def embed_text(text):
    resp = bedrock.invoke_model(
        modelId=EMBED_MODEL_ID,
        body=json.dumps({"inputText": text})
    )
    body = json.loads(resp["body"].read())
    return body["embedding"]


def main():
    with open(DOCS_PATH, "r") as f:
        content = f.read()

    # One chunk per paragraph (split on blank lines)
    chunks = [c.strip() for c in content.split("\n\n") if c.strip()]

    print(f"Found {len(chunks)} chunks to embed.")

    for i, chunk_text in enumerate(chunks):
        vector = embed_text(chunk_text)
        # DynamoDB requires Decimal, not float, for numeric types
        vector_decimal = [Decimal(str(v)) for v in vector]

        table.put_item(Item={
            "chunk_id": f"chunk-{i}",
            "text": chunk_text,
            "vector": vector_decimal
        })
        print(f"Ingested chunk-{i}: {chunk_text[:60]}...")

    print("Done.")


if __name__ == "__main__":
    main()
