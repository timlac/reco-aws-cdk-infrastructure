import os
import json
import boto3

from utils import generate_response
from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY

from surveys.survey_repository import SurveyRepository

from aws_lambda_powertools import Logger

# Initialize the AWS SDK clients
dynamodb = boto3.resource('dynamodb')
logger = Logger()


def handler(event, context):
    project_name = event['pathParameters'][PROJECT_NAME_KEY]
    # Retrieve data from the event
    data = json.loads(event["body"])

    try:
        survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])

        survey_id = survey_repo.create_survey(project_name, data)
        response_item = survey_repo.get_survey(project_name, survey_id)

        logger.info("Data inserted successfully: {}".format(response_item))
        return generate_response(200, response_item)

    except Exception as e:
        logger.error(str(e))
        return generate_response(500, "Error inserting data: {}".format(str(e)))
