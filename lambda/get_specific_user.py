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

    user_id = event['pathParameters']['userId']

    logger.info("event['pathParameters']: ", event['pathParameters'])

    logger.info("user id: ", user_id)

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    try:
        response = table.scan(
            FilterExpression=Attr("id").eq(user_id)
        )
        items = response.get('Items', [])

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
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(str(e))
        }
