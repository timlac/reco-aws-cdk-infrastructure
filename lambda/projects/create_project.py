import os
import json
from aws_lambda_powertools import Logger


from utils import generate_response
from constants import TABLE_NAME_KEY
from projects.project_repository import ProjectRepository


logger = Logger()


def handler(event, context):
    # Retrieve data from the event
    data = json.loads(event["body"])

    logger.info("logging data:")
    logger.info(data)

    project_repo = ProjectRepository(os.environ[TABLE_NAME_KEY])

    try:
        project_name = project_repo.create_project(data)

        response_item = project_repo.get_project(project_name)

        logger.info("Data inserted successfully: {}".format(response_item))
        return generate_response(200, body=response_item)

    except Exception as e:
        logger.error("Error inserting data: {}".format(str(e)))
        return generate_response(500, body="Error inserting data {}".format(str(e)))
