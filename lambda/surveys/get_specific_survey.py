import os

from constants import PROJECT_NAME_KEY, SURVEY_ID_KEY, TABLE_NAME_KEY
from utils import generate_response
from surveys.survey_repository import SurveyRepository


def handler(event, context):

    survey_id = event['pathParameters'][SURVEY_ID_KEY]
    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])

    try:
        response_item = survey_repo.get_survey(project_name, survey_id)

        return generate_response(200, response_item)

    except Exception as e:
        print(e)
        return generate_response(500, str(e))
