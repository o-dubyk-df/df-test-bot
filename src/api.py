import json
import logging
import os

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")  # Required

sqs = boto3.resource("sqs")
queue = sqs.Queue(SQS_QUEUE_URL)


def api_handler(event, context):
    """Receives Telegram update message."""

    logger.info("event: {}".format(json.dumps(event)))

    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return {"statusCode": 500, "body": "Invalid JSON payload."}

    message = {
        "update_id": body["update_id"],
        "message": {
            "message_id": body["message"]["message_id"],
            "chat": {
                "id": body["message"]["chat"]["id"],
                "type": body["message"]["chat"]["type"],
            },
            "date": body["message"]["date"],
            "text": body["message"]["text"],
        },
    }

    try:
        queue.send_message(MessageBody=json.dumps(message))
        return {"statusCode": 200, "body": "Success"}
    except Exception as exc:
        logger.exception(exc)
        return {"statusCode": 500, "body": exc.args}
