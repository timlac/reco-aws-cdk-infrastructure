import boto3
import json
import os
from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key
from cors_headers import cors_headers

from serializer import to_serializable

logger = Logger()


def handler(event, context):
    survey_name = event['pathParameters']['survey_name']

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
            KeyConditionExpression=Key('survey_name').eq(survey_name)
        )
        items = response['Items']

        logger.info("retrieved items")

        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps(items, default=to_serializable)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
