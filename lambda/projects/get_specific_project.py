import os
from aws_lambda_powertools import Logger

from utils import generate_response
from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY
from projects.project_repository import ProjectRepository


logger = Logger()


def handler(event, context):
    print("project name key is " + PROJECT_NAME_KEY)

    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    project_repo = ProjectRepository(os.environ[TABLE_NAME_KEY])

    try:
        response_item = project_repo.get_project(project_name)
        return generate_response(200, response_item)

    except Exception as e:
        print(e)
        return generate_response(500, str(e))
