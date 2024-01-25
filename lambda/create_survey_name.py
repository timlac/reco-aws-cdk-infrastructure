import os
import json
import boto3
from serializer import to_serializable
from survey_types import survey_types
from cors_headers import cors_headers
from aws_lambda_powertools import Logger

# Initialize the AWS SDK clients
dynamodb = boto3.resource('dynamodb')
logger = Logger()


def handler(event, context):

    survey_name = event['pathParameters']['survey_name']

    # Retrieve data from the event
    data = json.loads(event["body"])

    logger.info("logging data:")
    logger.info(data)

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    try:
        survey_type = data['survey_type']

        if survey_type not in survey_types:
            raise Exception("Invalid response type")

        # Insert data into the DynamoDB table
        table.put_item(
            Item={
                "survey_name": survey_name,
                "s3_data_folder": data['s3_data_folder'],
                "survey_type": data['survey_type'],
                "reply_meta": data['reply_meta'],
            },
            ConditionExpression="attribute_not_exists(survey_name)",  # Check if 'id' does not already exist
        )

        response = table.get_item(
            Key={
                "survey_name": survey_name,
            }
        )
        item = response.get('Item')  # Get the single item

        # logger.info("Data inserted successfully: {}".format(response))
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(item, default=to_serializable)
        }
    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps("Error inserting data")
        }
