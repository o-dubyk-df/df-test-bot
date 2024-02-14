# Telegram simple bot

## Local development

### Prerequisites

#### [Localstack installation](https://docs.localstack.cloud/getting-started/installation/)

```
python3 -m pip install --upgrade localstack
```

start localstack
```
localstack start
```

#### [AWS CLI integration](https://docs.localstack.cloud/user-guide/integrations/aws-cli/)

#### [AWS SAM integration](https://docs.localstack.cloud/user-guide/integrations/aws-sam/)

```
pip install aws-sam-cli-local
```

### Deploy to localstack

build
```
samlocal build -u
```

deploy
```
samlocal deploy --template .aws-sam/build/template.yaml --resolve-s3 --capabilities CAPABILITY_IAM --stack-name serverless-telegram-bot-test
```