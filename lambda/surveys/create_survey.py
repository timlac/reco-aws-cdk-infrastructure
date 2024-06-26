import os
import json
from pydantic import ValidationError

from projects.project_repository import ProjectRepository
from projects.project_model import ProjectModel
from surveys.database.survey_model import SurveyItemModel, SurveyModel

from surveys.database.survey_repository import SurveyRepository
from surveys.filename_sampling.sample_filenames import sample_filenames


from utils import generate_response, generate_id
from constants import PROJECT_NAME_KEY


survey_repo = SurveyRepository(os.environ["SURVEY_TABLE_NAME"])
project_repo = ProjectRepository(os.environ["PROJECT_TABLE_NAME"])


def generate_survey_items(project_name, valence):
    surveys_data = survey_repo.get_surveys(project_name, generate_meta=False)
    project = project_repo.get_project(project_name, generate_meta=False)

    project_model = ProjectModel(**project)
    surveys = [SurveyModel(**data) for data in surveys_data]

    filenames, emotion_ids = sample_filenames(surveys,
                                              project_model,
                                              valence)
    survey_items = []
    for filename in filenames:
        survey_item_model = SurveyItemModel(filename=filename, has_reply=0, reply=[])
        survey_items.append(survey_item_model)

    return survey_items, emotion_ids


def handler(event, context):
    project_name = event['pathParameters'][PROJECT_NAME_KEY]
    # Retrieve data from the event
    data = json.loads(event["body"])

    survey_items, emotion_ids = generate_survey_items(project_name, data.get("valence", None))

    survey_id = generate_id()

    try:
        survey_model = SurveyModel(project_name=project_name,
                                   survey_id=survey_id,
                                   survey_items=survey_items,
                                   emotion_ids=emotion_ids,
                                   **data)
    except ValidationError as e:
        # Handle validation errors, for example, by logging or raising an error
        print(f"Validation Error: {e}")
        return generate_response(404, "validation error {}".format(str(e)))

    try:
        survey_repo.create_survey(survey_model)
        response_item = survey_repo.get_survey(project_name, survey_id)

        print("Data inserted successfully: {}".format(response_item))
        return generate_response(200, response_item)

    except Exception as e:
        print(str(e))
        return generate_response(500, "Error inserting data: {}".format(str(e)))
