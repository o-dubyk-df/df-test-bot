import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")

sqs = boto3.resource("sqs")
queue = sqs.Queue(SQS_QUEUE_URL)


def lambda_handler(event, context):
    try:
        event = json.loads(event["body"])
        del event["message"]["from"]
        event["message"]["chat"] = {
            "id": event["message"]["chat"]["id"],
            "type": event["message"]["chat"]["type"],
        }
        queue.send_message(MessageBody=json.dumps(event))
        return {"statusCode": 200, "body": "Success"}

    except Exception as exc:
        logger.error(f"Error: {exc}")
        return {"statusCode": 500, "body": "Failure"}
