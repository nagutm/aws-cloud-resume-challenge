import json
import os
import boto3


def get_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    table = get_table()
    response = table.update_item(
        Key={"id": "visits"},
        UpdateExpression="ADD #c :inc",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )
    new_count = int(response["Attributes"]["count"])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "https://resume-mufaddal.com",
        },
        "body": json.dumps({"count": new_count}),
    }