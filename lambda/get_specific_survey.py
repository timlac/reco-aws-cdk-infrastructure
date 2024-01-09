import boto3
import json
import os
from aws_lambda_powertools import Logger

from boto3.dynamodb.conditions import Attr

from serializer import to_serializable


logger = Logger()


def handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    survey_id = event['pathParameters']['survey_id']
    survey_type = event['pathParameters']['survey_type']

    logger.info(f'Received event: {event}')

    logger.info("\nsurvey_id: ")
    logger.info(survey_id)

    logger.info("\nsurvey_type: ")
    logger.info(survey_type)

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(
            Key={
                "survey_type": survey_type,
                'survey_id': survey_id
            }
        )
        item = response.get('Item')  # Get the single item

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(item, default=to_serializable)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(str(e))
        }
