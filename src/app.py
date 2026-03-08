
import json
import os
import boto3

TABLE_NAME = os.getenv("TABLE_NAME", "visitorCount")

def _get_table():
    # Construct the resource each time (or memoize after first call)
    dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-2"))
    return dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    table = _get_table()
    response = table.update_item(
        Key={'id': 'count'},
        UpdateExpression='ADD #c :inc',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':inc': 1},
        ReturnValues='UPDATED_NEW'
    )
    count = int(response["Attributes"]["count"])
    return {
        "statusCode": 200,
        "body": json.dumps({"count": count})
    }
