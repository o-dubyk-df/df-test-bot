include .env

start: ## Start stack
	localstack start -d
	samlocal build -u
	samlocal deploy \
		--template .aws-sam/build/template.yaml \
		--resolve-s3 \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides TelegramBotToken=${TELEGRAM_BOT_TOKEN} \
		--region us-east-1 \
		--stack-name serverless-telegram-bot
	echo "Local API URL is `samlocal list stack-outputs --stack-name serverless-telegram-bot --region us-east-1 --output json|jq '.[0]| select( .OutputKey == \"TelegramApi\" )| .OutputValue'` please use it for testing"

stop: ## Stop stack
	localstack stop

clean: ## Kill docker compose
	docker compose down -v
