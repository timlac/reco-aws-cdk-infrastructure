import boto3
import json
import os
from aws_lambda_powertools import Logger


from serializer import to_serializable

logger = Logger()


def scan_full_table(db_table, limit=None):
    ret = []
    resp = db_table.scan()
    ret += resp['Items']

    while 'LastEvaluatedKey' in resp:
        resp = db_table.scan(ExclusiveStartKey=resp['LastEvaluatedKey'])
        ret += resp['Items']

    return ret


def handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    logger.info("table:")
    logger.info(table_name)
    logger.info(table)

    try:
        logger.info("scanning table")
        # Scan table to retrieve all users
        # response = table.scan()
        items = scan_full_table(table)
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
