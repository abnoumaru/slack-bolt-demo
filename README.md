
## 各種手順

### .envを読み込む

```bash
source .env
```

### ECRレポジトリ作成ログ

```bash
% aws ecr create-repository --repository-name slack-bolt-demo --region ap-northeast-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
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
  --image-uri XXXXXXXXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/slack-bolt-demo:latest \
  --publish
```

## 参考

- Lambdaのデプロイまで
  - https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html
