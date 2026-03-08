
import json
import os
import boto3
from moto import mock_aws
from app import lambda_handler

# Ensure a region is set for boto3 when running locally
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-2")

# Import AFTER setting env vars to ensure boto3 picks them up
from app import lambda_handler

@mock_aws
def test_lambda_handler_increments_count():
    # Arrange: create a mocked DynamoDB table and seed an item
    dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
    table = dynamodb.create_table(
        TableName="visitorCount",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.put_item(Item={"id": "count", "count": 0})

    # Act
    resp = lambda_handler({}, {})
    body = json.loads(resp["body"])

    # Assert
    assert resp["statusCode"] == 200
    assert body["count"] == 1

