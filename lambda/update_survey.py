import os
import json
import boto3
import time  # Import the time module
from aws_lambda_powertools import Logger
from serializer import to_serializable

# Initialize the AWS SDK clients
dynamodb = boto3.resource('dynamodb')
logger = Logger()

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True
}


def get_response_404(message):
    return {
        "statusCode": 404,
        "headers": headers,
        "body": json.dumps(message)
    }


def item_has_reply(has_reply):
    print("has_reply", has_reply)

    if has_reply == 1:
        return True
    elif has_reply == 0:
        return False
    else:
        raise Exception("Error: Something went wrong, has_reply is {}".format(has_reply))


def handler(event, context):
    # User ID (primary key) associated with the items
    survey_id = event['pathParameters']['survey_id']
    survey_type = event['pathParameters']['survey_type']

    data = json.loads(event["body"])
    filename = data['filename']
    reply = data['reply']

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    # Step 2: Retrieve existing user's data
    response = table.get_item(
        Key={'id': survey_id}
    )

    # Check if the user exists (Item is native DynamoDB)
    if 'Item' not in response:
        return get_response_404('Error: survey {survey_id} does not exist'.format(survey_id))

    dynamo_item = response['Item']
    update_idx = None

    # items the user attribute for filename we seek user replies for
    for idx, item in enumerate(dynamo_item['survey_items']):

        if item['filename'] == filename:

            if item_has_reply(item['has_reply']):
                return get_response_404("Error: Reply already exists on user item.")
            item['reply'] = reply
            update_idx = idx

    if update_idx is None:
        return get_response_404("Error: Filename {} not found...".format(filename))

    try:
        table.update_item(
            Key={
                'survey_type': survey_type,
                'survey_id': survey_id
            },
            UpdateExpression=f'SET survey_items[{update_idx}].reply = :val, '
                             f'survey_items[{update_idx}].has_reply = :hasReplyVal',
            ExpressionAttributeValues={
                ':val': reply,
                ':hasReplyVal': 1
            }
        )

    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps("Error inserting data {}".format(str(e)))
        }

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps("Item was successfully updated!")
    }
