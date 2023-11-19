import os
import json
import boto3
import time  # Import the time module
from aws_lambda_powertools import Logger

# Initialize the AWS SDK clients
dynamodb = boto3.client('dynamodb')
logger = Logger()


def format_item(item):
    formatted_item = {
        "M":
            {
                "filename": {"S": item["filename"]},  # "S" for string
                "video_id": {"S": str(item["video_id"])},
                "emotion_id": {"S": str(item["emotion_id"])},  # "N" for number
                "reply": {"S": item["reply"]}
            }
    }
    return formatted_item


def handler(event, context):
    # Retrieve data from the event
    data = json.loads(event["body"])

    logger.info("logging data items")
    logger.info(data["items"])

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']

    # Convert the list of items into the DynamoDB L type
    items_with_attributes = [format_item(item) for item in data["items"]]

    logger.info("post attribute adding")
    logger.info(items_with_attributes)

    current_time = int(time.time())  # Convert to an integer timestamp
    try:
        # Insert data into the DynamoDB table
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                "id": {"S": data["alias"]},
                "items": {"L": items_with_attributes},
                "createdAt": {"N": str(str(current_time))},
                # Add other attributes here
            }
        )

        logger.info("Data inserted successfully: {}".format(response))
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps("Data inserted successfully")
        }
    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps("Error inserting data")
        }
