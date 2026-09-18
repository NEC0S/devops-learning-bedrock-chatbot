"""
Seeds a few sample orders into the orders DynamoDB table so the agent's
check_order_status tool has something real to look up. Safe to re-run.

Requires env var: TABLE_NAME
"""

import boto3
import os

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

SAMPLE_ORDERS = [
    {"order_id": "ORD-1001", "status": "Shipped", "item": "Wireless Headphones"},
    {"order_id": "ORD-1002", "status": "Processing", "item": "Standing Desk"},
    {"order_id": "ORD-1003", "status": "Delivered", "item": "Mechanical Keyboard"},
    {"order_id": "ORD-1004", "status": "Delayed - Weather", "item": "Smart Watch"},
]


def main():
    for order in SAMPLE_ORDERS:
        table.put_item(Item=order)
        print(f"Seeded {order['order_id']} ({order['status']})")
    print("Done.")


if __name__ == "__main__":
    main()
