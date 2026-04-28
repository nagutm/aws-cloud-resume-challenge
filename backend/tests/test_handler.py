import os
import json
import boto3
import pytest
from moto import mock_aws

# Set this BEFORE importing handler, since handler reads it inside get_table()
os.environ["TABLE_NAME"] = "test-resume-visits"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

import handler


@pytest.fixture
def dynamodb_table():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="test-resume-visits",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.put_item(Item={"id": "visits", "count": 0})
        yield table


def test_increments_from_zero(dynamodb_table):
    response = handler.lambda_handler({}, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["count"] == 1


def test_increments_multiple_times(dynamodb_table):
    handler.lambda_handler({}, None)
    handler.lambda_handler({}, None)
    response = handler.lambda_handler({}, None)

    body = json.loads(response["body"])
    assert body["count"] == 3


def test_response_includes_cors_header(dynamodb_table):
    response = handler.lambda_handler({}, None)
    assert response["headers"]["Access-Control-Allow-Origin"] == "https://resume-mufaddal.com"
    assert response["headers"]["Content-Type"] == "application/json"