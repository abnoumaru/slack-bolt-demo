
## 各種手順

### Slackアプリの設定

- OAuth & Permissions
  - Bot Token Scopesにchat:writeを追加
- Event Subscriptions
  - On にしてRequest URLにLambdaのエンドポイントを設定
  - Subscribe to bot eventsにapp_mentionを追加


### .envを読み込む

```bash
source .env
```

### ECRレポジトリ作成

```bash
% aws ecr create-repository --repository-name slack-bolt-demo --region ap-northeast-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

### IAMロール作成

```bash
aws iam create-role \
  --role-name slack-bolt-demo \
  --assume-role-policy-document file://trust-policy.json
```

```bash
aws iam attach-role-policy \
  --role-name slack-bolt-demo \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

```bash
aws iam attach-role-policy \
  --role-name slack-bolt-demo \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
```

### Lambda関数の作成

```bash
aws lambda create-function \
  --function-name slack-bolt-demo \
  --package-type Image \
  --code ImageUri=${ECR_URI}:latest \
  --role arn:aws:iam::${ACCOUNT_ID}:role/slack-bolt-demo \
  --region ap-northeast-1
```

### Lambda関数のイメージ更新

```bash
aws lambda update-function-code \
  --function-name slack-bolt-demo \
  --image-uri ${ECR_URI}:latest \
  --publish
```

## 参考

- Lambdaのデプロイまで
  - https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html
