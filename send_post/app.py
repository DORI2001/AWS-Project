import boto3
import json
import os
import re
from boto3.dynamodb.conditions import Key
from datetime import datetime
import random
import string

s3 = boto3.resource("s3")
bucket = s3.Bucket(os.environ["MESSAGES_BUCKET"])

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])


def lambda_handler(event, context):
    group_id = event["pathParameters"]["group-id"]
    message_details = json.loads(event["body"])
    # Check that group exists
    group_pk = f"GROUP#{group_id}"
    group_sk = "METADATA#"
    response = table.query(KeyConditionExpression=(Key('PK').eq(group_pk) & Key('SK').begins_with(group_sk)))
    if len(response["Items"]) == 0:
        return {"statusCode": 404, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": f"Group {group_id} not found"})}

    # Check that group has subscribers
    subscribers = table.query(KeyConditionExpression=(Key('PK').eq(group_pk) & Key('SK').begins_with("USER#")))
    if len(subscribers["Items"]) == 0:
        return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": "no_subscribers"})}

    now = datetime.now()
    date_folder = now.strftime("%Y/%m/%d")
    message_details["group_id"] = group_id
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=10))
    
    object_key = f"{group_id}/{date_folder}/{random_suffix}.json"
    body = json.dumps(message_details).encode()
    bucket.put_object(Key=object_key, Body=body)
    return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"}}
