# tests/test_app.py
import json
import os
import boto3
import moto

# Use a consistent region for moto/boto3
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-2")

@moto.mock_aws
def test_lambda_handler_increments_count():
    # ---- Arrange
    # 1) Set env vars your handler expects
    os.environ["TABLE_NAME"] = "visitorCount"

    # 2) Create the mocked table
    dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
    table = dynamodb.create_table(
        TableName=os.environ["TABLE_NAME"],
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.put_item(Item={"id": "count", "count": 0})

    # 3) Import AFTER moto + env are in place (important if app.py binds boto3 at import)
    from app import lambda_handler

    # ---- Act
    resp = lambda_handler({"requestContext": {"http": {"method": "GET"}}}, {})
    assert resp["statusCode"] == 200

    body = json.loads(resp["body"])

    # ---- Assert
    assert isinstance(body, dict)
    assert body["count"] == 1
    # (optional) assert content type if your lambda sets it:
    # assert resp["headers"]["content-type"] == "application/json"