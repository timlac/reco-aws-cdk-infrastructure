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
    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])
    survey = survey_repo.get_survey(project_name, survey_id)

    if not survey:
        return generate_response(404, 'Error: survey {} does not exist'.format(survey_id))

    survey_model = SurveyModel(**survey)
    print("survey model loaded")
    print(survey_model)

    data = json.loads(event["body"])
    allowed_updates = {'sex', 'date_of_birth', "consent"}
    filtered_updates = {k: v for k, v in data.items() if k in allowed_updates}

    print("filtered updates: {}".format(filtered_updates))
    updated_survey_model = survey_model.copy(update=filtered_updates)

    print("updated survey model: {}".format(updated_survey_model))

    try:
        survey_repo.update_survey(updated_survey_model)

    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return generate_response(500, "Error inserting data: {}".format(str(e)))

    return generate_response(200, "Survey was successfully updated!")
