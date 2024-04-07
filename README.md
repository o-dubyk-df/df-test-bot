# Test serverless telegram bot

## Local Development

1. Install and setup [localstack](https://docs.localstack.cloud/getting-started/installation/)
2. define variables in .env
3. `make start`
4. Grab stack output to get api endpoint

### Testing
Test the code:
```
ruff check & python -m unittest src/tests.py
```

Test the bot:
```
curl  -i -k -XPOST https://fc9c1488.execute-api.us-east-1.localhost.localstack.cloud/ -d '{"update_id":813352806,"message":{"message_id":186,"from":{"id":879487978,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":879487978,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"hello"}}' -H 'Content-Type: application/json'
```


### Tasks for test

1. Modify the code so that the bot only responds to the “/hello” command or any message containing “hello” in any case.
2. The bot must respond to any other text message: Sorry, I don’t understand.
3. Ensure that the SQS queue does not receive the full Telegram payload but instead only the minimal data required to generate a message to the client in the Lambda function sqs.py.
4. Additionally, create unit tests for both AWS Lambda functions: api.py and sqs.py.
