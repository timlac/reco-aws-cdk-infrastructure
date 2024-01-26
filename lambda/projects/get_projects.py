import os
from constants import TABLE_NAME_KEY
from projects.project_repository import ProjectRepository
from utils import generate_response


def handler(event, context):
    project_repo = ProjectRepository(os.environ[TABLE_NAME_KEY])

    try:
        response_items = project_repo.get_projects()
        return generate_response(200, response_items)

    except Exception as e:
        print(e)
        return generate_response(500, str(e))
