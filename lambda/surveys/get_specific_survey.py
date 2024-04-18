import os

from constants import PROJECT_NAME_KEY, SURVEY_ID_KEY
from utils import generate_response
from surveys.database.survey_repository import SurveyRepository
from projects.project_repository import ProjectRepository


def handler(event, context):
    """
    This function queries both the project database and the survey database
    and returns both project data and survey data.
    """

    survey_id = event['pathParameters'][SURVEY_ID_KEY]
    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    survey_repo = SurveyRepository(os.environ["SURVEY_TABLE_NAME"])
    project_repo = ProjectRepository(os.environ["PROJECT_TABLE_NAME"])

    try:
        survey_response_item = survey_repo.get_survey(project_name, survey_id)
        project_response_item = project_repo.get_project(project_name, generate_meta=False)
        survey_response_item.update(project_response_item)

        # remove this large value to improve performance
        survey_response_item["s3_experiment_objects"] = None

        return generate_response(200, survey_response_item)

    except Exception as e:
        print(e)
        return generate_response(500, str(e))
