import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

sqs = boto3.resource('sqs')
queue = sqs.Queue(SQS_QUEUE_URL)

def lambda_handler(event, context):
    logger.info("event: {}".format(json.dumps(event)))
    try:    
        body = event.get("body", "")
        
        if "/hello" in body or "/start" in body or "hello" in body.lower():
            message = body
        else:
            message = "I don't understand"
        
        queue.send_message(MessageBody=message)

        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as exc:
        return {
            'statusCode': 500,
            'body': 'Failure'
        }

