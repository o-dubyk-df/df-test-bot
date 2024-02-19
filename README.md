# Test telegram bot

## Local Development

### [localstack](https://docs.localstack.cloud/getting-started/installation/)

### Deployment to localstack

```
samlocal build -u && samlocal deploy --template .aws-sam/build/template.yaml --resolve-s3 --capabilities CAPABILITY_IAM --parameter-overrides TelegramBotToken="{TELEGRAM BOT TOKEN}" --region us-east-1 --stack-name serverless-telegram-bot
```

grab stack output to get api endpoint

### Testing

```
curl  -i -k -XPOST https://fc9c1488.execute-api.us-east-1.localhost.localstack.cloud/ -d '{"update_id":813352806,"message":{"message_id":186,"from":{"id":879487978,"is_bot":false,"first_name":"Test","last_name":"Test","language_code":"uk"},"chat":{"id":879487978,"first_name":"Test","last_name":"Test","type":"private"},"date":1708367401,"text":"hello"}}' -H 'Content-Type: application/json'
```
