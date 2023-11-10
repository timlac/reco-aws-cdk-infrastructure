import os
import json
import boto3
import time  # Import the time module
from aws_lambda_powertools import Logger

# Initialize the AWS SDK clients
dynamodb = boto3.client('dynamodb')
logger = Logger()


def handler(event, context):
    # Retrieve data from the event
    data = json.loads(event["body"])

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']

    current_time = int(time.time())  # Convert to an integer timestamp

    try:
        # Insert data into the DynamoDB table
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                "id": {"S": data["id"]},
                "createdAt": {"N": str(str(current_time))},
                # Add other attributes here
            }
        )

        logger.info("Data inserted successfully: {}".format(response))
        return {
            "statusCode": 200,
            "body": json.dumps("Data inserted successfully")
        }
    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return {
            "statusCode": 500,
            "body": json.dumps("Error inserting data")
        }
