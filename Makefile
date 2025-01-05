include .env
.PHONY: build run test

APP_NAME=slack-bolt-demo
IMAGE_TAG=test

build:
	docker build --platform linux/amd64 -t $(APP_NAME):$(IMAGE_TAG) .

run:
	docker run --platform linux/amd64 --env-file .env -p 9000:8080 $(APP_NAME):$(IMAGE_TAG)

test:
	curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

push: build
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $(ECR_URI)
	docker tag $(APP_NAME):$(IMAGE_TAG) $(ECR_URI):latest
	docker push $(ECR_URI):latest
