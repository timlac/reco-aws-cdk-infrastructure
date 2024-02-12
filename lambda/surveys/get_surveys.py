import os

from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY
from surveys.database.survey_model import SurveyModel
from utils import generate_response
from surveys.database.survey_repository import SurveyRepository
from surveys.database.survey_item_handler import set_progress

def scan_full_table(db_table, limit=None):
    ret = []
    resp = db_table.scan()
    ret += resp['Items']

    while 'LastEvaluatedKey' in resp:
        resp = db_table.scan(ExclusiveStartKey=resp['LastEvaluatedKey'])
        ret += resp['Items']

    return ret


def handler(event, context):
    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])

    try:
        response_items = survey_repo.get_surveys(project_name)

        # setting the progress variable
        survey_models = [SurveyModel(**item) for item in response_items]
        set_progress(survey_models)
        ret = [survey.dict() for survey in survey_models]

        return generate_response(200, ret)

    except Exception as e:
        print(e)
        return generate_response(500, str(e))
