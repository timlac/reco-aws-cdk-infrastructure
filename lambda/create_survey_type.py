# import os
# import json
# import boto3
# import time  # Import the time module
# import datetime
# from zoneinfo import ZoneInfo
# from generate_survey_id import generate_id
# from serializer import to_serializable
# from survey_types import survey_types
#
# from aws_lambda_powertools import Logger
#
# # Initialize the AWS SDK clients
# dynamodb = boto3.resource('dynamodb')
# logger = Logger()
#
#
# def handler(event, context):
#
#     survey_type = event['pathParameters']['survey_type']
#
#     # Retrieve data from the event
#     data = json.loads(event["body"])
#
#     logger.info("logging data:")
#     logger.info(data)
#
#     # Retrieve the DynamoDB table name from the environment variables
#     table_name = os.environ['DYNAMODB_TABLE_NAME']
#     table = dynamodb.Table(table_name)
#
#     try:
#         if survey_type not in survey_types:
#             raise Exception("Invalid response type")
#
#         # Insert data into the DynamoDB table
#         table.put_item(
#             Item={
#                 "survey_type": survey_type,
#                 "s3_bucket": data['data_folder'],
#                 "user_id": data["user_id"],
#                 "survey_items": survey_items_with_attributes,
#                 "emotion_alternatives": data["emotion_alternatives"],
#                 "valence": data["valence"],
#                 "created_at": current_date,
#                 "date_of_birth": str(data["date_of_birth"]),
#                 "sex": data["sex"],
#                 "reply_format": data["reply_format"]
#             },
#             ConditionExpression="attribute_not_exists(id)",  # Check if 'id' does not already exist
#         )
#
#         response = table.get_item(
#             Key={
#                 "survey_type": survey_type,
#                 'survey_id': survey_id
#             }
#         )
#         item = response.get('Item')  # Get the single item
#
#         # logger.info("Data inserted successfully: {}".format(response))
#         return {
#             "statusCode": 200,
#             "headers": {
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Credentials": True
#             },
#             "body": json.dumps(item, default=to_serializable)
#         }
#     except Exception as e:
#         logger.error("Error inserting data: {}".format(str(e)))
#         return {
#             "statusCode": 500,
#             "headers": {
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Credentials": True
#             },
#             "body": json.dumps("Error inserting data")
#         }
