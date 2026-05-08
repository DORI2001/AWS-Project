import boto3
import json
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])


def lambda_handler(event, context):
    group_id = event["pathParameters"]["group-id"]
    group_pk = f"GROUP#{group_id}"

    # Get all items for this group (metadata + subscribers)
    response = table.query(KeyConditionExpression=Key("PK").eq(group_pk))
    items = response["Items"]

    if not items:
        return {"statusCode": 404, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": f"Group {group_id} not found"})}

    with table.batch_writer() as batch:
        for item in items:
            # Delete GROUP#{group_id} / METADATA# and GROUP#{group_id} / USER#{email}
            batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})
            # Also delete the reverse USER#{email} / group_id mapping
            if item["SK"].startswith("USER#"):
                email = item["SK"].split("#")[1]
                batch.delete_item(Key={"PK": f"USER#{email}", "SK": group_id})

    return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"deleted": group_id})}
