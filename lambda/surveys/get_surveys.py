import os

from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY
from utils import generate_response
from surveys.survey_repository import SurveyRepository


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
        return generate_response(200, response_items)

    except Exception as e:
        print(e)
        return generate_response(500, str(e))
