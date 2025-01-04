import os
import re
import logging
import boto3
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from botocore.exceptions import ClientError

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DynamoDBクライアントの作成
dynamodb = boto3.client("dynamodb")
table_name = os.environ.get("DYNAMO_DB_TABLE")

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    # app_mentionを処理した後sayする前にLambdaが終了しないようにする
    process_before_response=True,
)
receiver = SlackRequestHandler(app)


@app.event("app_mention")
def onAppMention(event, say):
    logger.info(f"Received event: {event}")
    textWithoutMention = re.sub(r"^<@(.+?)>", "", event["text"]).strip()

    # DynamoDBからアイテムを取得
    try:
        response = dynamodb.get_item(
            TableName=table_name, Key={"PrimaryKey": {"S": textWithoutMention}}
        )
        item = response.get("Item")
        if item:
            item_text = "\n".join([f"{k}: {v['S']}" for k, v in item.items()])
            say(
                channel=event["channel"],
                thread_ts=event["event_ts"],
                text=f"Item found:\n{item_text}",
            )
        else:
            say(
                channel=event["channel"],
                thread_ts=event["event_ts"],
                text="Item not found.",
            )
    except ClientError as e:
        logger.error(f"Unable to get item: {e}")
        say(
            channel=event["channel"],
            thread_ts=event["event_ts"],
            text="Error retrieving item from DynamoDB.",
        )


def handler(event, context):
    return receiver.handle(event, context)
