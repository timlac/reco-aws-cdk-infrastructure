import os
import json
import boto3

from projects.project_repository import ProjectRepository
from utils import generate_response
from constants import PROJECT_NAME_KEY

from surveys.survey_repository import SurveyRepository
from surveys.filename_sampling.sample_filenames import sample_filenames
from pydantic import BaseModel

from aws_lambda_powertools import Logger

# os.environ['AWS_PROFILE'] = 'rackspaceAcc'


# Initialize the AWS SDK clients
dynamodb = boto3.resource('dynamodb')
logger = Logger()


survey_repo = SurveyRepository(os.environ["SURVEY_TABLE_NAME"])
project_repo = ProjectRepository(os.environ["PROJECT_TABLE_NAME"])

# survey_repo = SurveyRepository("EmotionDataStack-dev-surveytable310F762D-1SADR68QRMPOO")
# project_repo = ProjectRepository("EmotionDataStack-dev-projecttable27032958-GVCRDU4JG31B")


class ProjectMeta(BaseModel):
    s3_experiment_objects: list[str]
    samples_per_survey: int
    balanced_sampling_enabled: bool
    emotions_per_survey: int


def generate_survey_items(project_name, valence):
    survey_response_items = survey_repo.get_surveys(project_name)
    project_response_item = project_repo.get_project(project_name, generate_meta=False)

    project_meta = ProjectMeta(**project_response_item)

    filenames, emotion_ids = sample_filenames(survey_response_items,
                                              project_meta,
                                              valence)

    survey_items = []
    for filename in filenames:
        survey_item = {
            "filename": filename,
            "reply": [],
            "has_reply": 0
        }
        survey_items.append(survey_item)

    print(survey_items)


# generate_survey_items("SingleProj", "pos")
#
#
# # TODO: Need to be able to specify the distribution of emotions....
#
# # TODO: Either include parameter whether to create survey items in body, or use some other kind of parameter...


def handler(event, context):
    project_name = event['pathParameters'][PROJECT_NAME_KEY]
    # Retrieve data from the event
    data = json.loads(event["body"])

    # valence = data.get("valence", None)

    try:

        survey_id = survey_repo.create_survey(project_name, data)
        response_item = survey_repo.get_survey(project_name, survey_id)

        logger.info("Data inserted successfully: {}".format(response_item))
        return generate_response(200, response_item)

    except Exception as e:
        logger.error(str(e))
        return generate_response(500, "Error inserting data: {}".format(str(e)))
