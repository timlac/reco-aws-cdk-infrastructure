import json
import os
from projects.project_repository import ProjectRepository
from surveys.database.survey_model import SurveyModel
from surveys.database.survey_repository import SurveyRepository
from utils import get_emotion_id
from projects.project_model import ProjectModel
from surveys.filename_sampling.sample_filenames import sample_filenames
from time import time

start = time()


os.environ['AWS_PROFILE'] = 'rackspaceAcc'

survey_repo = SurveyRepository("EmotionDataStack-dev-surveytable310F762D-1SADR68QRMPOO")
project_repo = ProjectRepository("EmotionDataStack-dev-projecttable27032958-GVCRDU4JG31B")

project_name = "appraisal_study"
stop = time()

duration = stop - start

print(f"duration: {duration}")

start = time()

survey_response_items = survey_repo.get_surveys(project_name, generate_meta=False)

stop = time()

duration = stop - start

print(f"duration: {duration}")
start = time()

project_response_item = project_repo.get_project(project_name, generate_meta=False)

project_model = ProjectModel(**project_response_item)

surveys = [SurveyModel(**data) for data in survey_response_items]

print(len(surveys))

stop = time()

duration = stop - start

print(f"duration: {duration}")

start = time()

filenames, emotion_ids = sample_filenames(surveys,
                                          project_model,
                                          None)

stop = time()

duration = stop - start

print(f"duration: {duration}")

#
# print(filenames)
# counts = {}
# for filename in filenames:
#     emotion_id = get_emotion_id(filename)
#     if emotion_id in counts:
#         counts[emotion_id] += 1
#     else:
#         counts[emotion_id] = 1
#
# for i in counts.items():
#     print(i)
