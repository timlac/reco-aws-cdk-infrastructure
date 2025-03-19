import json
import os
from time import time
from projects.project_repository import ProjectRepository
from surveys.database.survey_repository import SurveyRepository
from surveys.database.survey_model import SurveyModel

from surveys.get_item_stats import handler
# Set AWS Profile
os.environ['AWS_PROFILE'] = 'rackspaceAcc'

os.environ["DYNAMODB_TABLE_NAME"] = "EmotionDataStack-dev-surveytable310F762D-1SADR68QRMPOO"

# Initialize repositories
survey_repo = SurveyRepository("EmotionDataStack-dev-surveytable310F762D-1SADR68QRMPOO")
project_repo = ProjectRepository("EmotionDataStack-dev-projecttable27032958-GVCRDU4JG31B")

# Define project name
project_name = "appraisal_study"

# Measure time for setup
start = time()
stop = time()
print(f"Setup duration: {stop - start:.4f} seconds")

# Measure time for local survey fetch
start = time()
survey_response_items = survey_repo.get_surveys(project_name, generate_meta=False)
stop = time()
print(f"Local DB fetch duration: {stop - start:.4f} seconds")


all_items = []

for item in survey_response_items:
    survey = SurveyModel(**item)

    row = {
        "project_name": survey.project_name,
        "survey_name": survey.survey_name,
        "survey_id": survey.survey_id,
        "survey_items": len(survey.survey_items)
    }

    all_items.extend(survey.survey_items)

print(f"Total items: {len(all_items)}")


# # Measure time for calling the Lambda handler locally
# start = time()
#
# mock_event = {
#     "pathParameters": {"project_name": project_name}
# }
#
#
# mock_context = {}  # AWS Lambda context is usually not needed
#
# response = handler(mock_event, mock_context)  # Directly invoke your function
#
# stop = time()
# print(f"Handler execution duration: {stop - start:.4f} seconds")
#
# # Print the response for debugging
# print("Lambda Handler Response:", json.dumps(response, indent=2))
