import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")

sqs = boto3.resource("sqs")
queue = sqs.Queue(SQS_QUEUE_URL)

{
    "update_id": 813352806,
    "message": {
        "message_id": 186,
        "chat": {"id": 123, "type": "private"},
        "date": 1708367401,
        "text": "11122 2hhheeellooo3332 3222",
    },
}


def lambda_handler(event, context):
    try:
        event = json.loads(event["body"])
        event = {
            "update_id": event["update_id"],
            "message": {
                "message_id": event["message"]["message_id"],
                "chat": {
                    "id": event["message"]["chat"]["id"],
                    "type": event["message"]["chat"]["type"],
                },
                "date": event["message"]["date"],
                "text": event["message"]["text"],
            },
        }
        queue.send_message(MessageBody=json.dumps(event))
        return {"statusCode": 200, "body": "Success"}

    except Exception as exc:
        logger.error(f"Error: {exc}")
        return {"statusCode": 500, "body": "Failure"}
