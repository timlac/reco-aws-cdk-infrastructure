import os
import json
from aws_lambda_powertools import Logger
from pydantic import ValidationError
from surveys.database.survey_model import SurveyModel, SurveyItemModel
from utils import generate_response
from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY, SURVEY_ID_KEY

from surveys.database.survey_repository import SurveyRepository

from surveys.database.survey_item_handler import get_filename_index

logger = Logger()


def handler(event, context):
    survey_id = event['pathParameters'][SURVEY_ID_KEY]
    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    data = json.loads(event["body"])
    filename = data.get('filename')
    reply = data.get('reply', [])

    # Use SurveyItemModel to validate reply
    try:
        # Create a temporary SurveyItemModel instance for validation
        SurveyItemModel(filename=filename, has_reply=0, reply=reply)
    except ValidationError as e:
        # ValidationError will be raised if 'reply' is not a list
        return generate_response(400, f"Invalid reply format: {e.json()}")

    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])
    survey = survey_repo.get_survey(project_name, survey_id)

    if not survey:
        return generate_response(404, 'Error: survey {} does not exist'.format(survey_id))

    try:
        survey_model = SurveyModel(**survey)
        filename_idx = get_filename_index(survey_model.survey_items, filename)
    except Exception as e:
        return generate_response(404, str(e))

    try:
        survey_repo.update_survey(project_name, survey_id, filename_idx, reply)

    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return generate_response(500, "Error inserting data: {}".format(str(e)))

    return generate_response(200, "Item was successfully updated!")
