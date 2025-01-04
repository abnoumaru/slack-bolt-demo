.PHONY: build run test

APP_NAME=slack-bolt-demo
IMAGE_TAG=test
ECR_URI=XXXXXXXXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/$(APP_NAME)

build:
	docker build --platform linux/amd64 -t $(APP_NAME):$(IMAGE_TAG) .

run:
	docker run --platform linux/amd64 --env-file .env -p 9000:8080 $(APP_NAME):$(IMAGE_TAG)

test:
	curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

push: build
	aws ecr get-login-password | docker login --username AWS --password-stdin $(ECR_URI)
	docker tag $(APP_NAME):$(IMAGE_TAG) $(ECR_URI):latest
	docker push $(ECR_URI):latest
