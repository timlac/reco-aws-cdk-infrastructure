import os
import json
from aws_lambda_powertools import Logger
from utils import generate_response
from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY, SURVEY_ID_KEY

from surveys.survey_repository import SurveyRepository

from surveys.survey_item_handler import get_filename_index

logger = Logger()


def handler(event, context):
    survey_id = event['pathParameters'][SURVEY_ID_KEY]
    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    data = json.loads(event["body"])
    filename = data['filename']
    reply = data['reply']

    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])
    survey = survey_repo.get_survey(project_name, survey_id)

    print("survey: ", survey)

    if not survey:
        return generate_response(404, 'Error: survey {} does not exist'.format(survey_id))

    try:
        filename_idx = get_filename_index(survey.get("survey_items"), filename)
    except Exception as e:
        return generate_response(404, str(e))

    try:
        survey_repo.update_survey(project_name, survey_id, filename_idx, reply)

    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return generate_response(500, "Error inserting data: {}".format(str(e)))

    return generate_response(200, "Item was successfully updated!")
