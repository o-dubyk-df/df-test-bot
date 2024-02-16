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
        # queue.send_message(MessageBody=event["body"])
        # return {
        #     'statusCode': 200,
        #     'body': 'Success'
        # }

        if "message" in event and ("text" in event["message"] or "entities" in event["message"]):
            chat_id = event["message"]["chat"]["id"]
            text = event["message"].get("text", "")
            
            if "entities" in event["message"] and event["message"]["entities"][0]["type"] == "bot_command":
                command = text.split()[0]
                if command in ["/hello", "/start"]:

                    message_to_send = {
                        'chat_id': chat_id,
                        'message': text
                    }
                
                else:

                    message_to_send = {
                        'chat_id': chat_id,
                        'message': "I don’t understand"
                    }
            
            elif "hello" in text.lower():

                message_to_send = {
                    'chat_id': chat_id,
                    'message': text
                }
                
            else:

                message_to_send = {
                    'chat_id': chat_id,
                    'message': "I don't understand"
                }
       
        else:
        
            message_to_send = {
                'chat_id': None,
                'message': "I don't understand"
            }

        queue.send_message(MessageBody=json.dumps(message_to_send))
        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as exc:
        return {
            'statusCode': 500,
            'body': 'Failure'
        }

