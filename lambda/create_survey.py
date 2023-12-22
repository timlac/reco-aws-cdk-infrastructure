import os
import json
import boto3
import time  # Import the time module
import datetime
from zoneinfo import ZoneInfo
from generate_survey_id import generate
from serializer import to_serializable

from aws_lambda_powertools import Logger

# Initialize the AWS SDK clients
dynamodb = boto3.resource('dynamodb')
logger = Logger()


def format_item(item):

    if "reply" in item:
        reply = item["reply"]
    else:
        reply = {}

    if "has_reply" in item:
        has_reply = item["has_reply"]
    else:
        has_reply = 0

    formatted_item = {
        "M":
            {
                "filename": {"S": item["filename"]},  # "S" for string
                "video_id": {"S": str(item["video_id"])},
                "emotion_id": {"S": str(item["emotion_id"])},  # "N" for number
                "reply": {"M": reply},
                "has_reply": {"N": str(has_reply)}
            }
    }
    return formatted_item


def handler(event, context):
    # Retrieve data from the event
    data = json.loads(event["body"])

    logger.info("logging data:")
    logger.info(data)

    logger.info("logging data items:")
    logger.info(data["survey_items"])

    # Retrieve the DynamoDB table name from the environment variables
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)

    # Convert the list of items into the DynamoDB L type
    survey_items_with_attributes = [format_item(item) for item in data["survey_items"]]
    emotion_alternatives = [{"S": emotion_id} for emotion_id in data["emotion_alternatives"]]

    logger.info("post attribute adding")
    logger.info(survey_items_with_attributes)

    logger.info("sex")
    logger.info(data["sex"])

    current_date = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())  # Convert to an integer timestamp

    try:
        survey_id = generate()

        # Insert data into the DynamoDB table
        table.put_item(
            Item={
                "id": {"S": survey_id},
                "user_id": {"S": data["user_id"]},
                "survey_items": {"L": survey_items_with_attributes},
                "emotion_alternatives": {"L": emotion_alternatives},
                "valence": {"S": data["valence"]},
                "created_at": {"S": current_date},
                "date_of_birth": {"S": str(data["date_of_birth"])},
                "sex": {"S": data["sex"]}
                # Add other attributes here
            },
            ConditionExpression="attribute_not_exists(id)",  # Check if 'id' does not already exist
        )

        response = table.get_item(
            Key={
                'id': survey_id
            }
        )
        item = response.get('Item')  # Get the single item

        logger.info("Data inserted successfully: {}".format(response))
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps(item, default=to_serializable)
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
