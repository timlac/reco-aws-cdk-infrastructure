import boto3
import json
import os
from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key


from serializer import to_serializable

logger = Logger()


def set_progress(items):
    for idx, survey in enumerate(items):
        count = sum(1 for item in survey["survey_items"] if item["has_reply"] == 1)
        total = len(survey["survey_items"])

        items[idx]["progress"] = count / total
    return items


def set_accuracy(items):
    for idx, survey in enumerate(items):
        count = sum(1 for item in survey["survey_items"] if item["emotion_id"] == item["reply"])
        total = len(survey["survey_items"])

        items[idx]["accuracy"] = count / total
    return items


# def set_metadata(items):
#     metadata = []
#     for idx, survey in enumerate(items):
#         for survey_item in survey["survey_items"]:
#             meta = survey_item["filename"]
#             metadata.append(meta)


def scan_full_table(db_table, limit=None):
    ret = []
    resp = db_table.scan()
    ret += resp['Items']

    while 'LastEvaluatedKey' in resp:
        resp = db_table.scan(ExclusiveStartKey=resp['LastEvaluatedKey'])
        ret += resp['Items']

    return ret


def handler(event, context):
    survey_type = event['pathParameters']['survey_type']

    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    try:
        logger.info("scanning table")
        # Scan table to retrieve all users
        # response = table.scan()

        response = table.query(
            KeyConditionExpression=Key('survey_type').eq(survey_type)
        )
        items = response['Items']

        logger.info("retrieved items")

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(items, default=to_serializable)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
