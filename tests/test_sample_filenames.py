import json
import os
from projects.project_repository import ProjectRepository
from surveys.database.survey_repository import SurveyRepository
from utils import get_emotion_id
from projects.project_model import ProjectModel
from surveys.filename_sampling.sample_filenames import sample_filenames

#
#
# path = "data/project_data.json"
#
# # path = "../../../te"
#
# with open(path) as json_data:
#     d = json.load(json_data)
#     json_data.close()
#
# print(d["samples_per_survey"])
#
# pm = ProjectModel(**d)
#
# pm.samples_per_survey = 900
#
# pm.emotions_per_survey = 22
#
# filenames, eids = sample_filenames([], pm, None)
#
# counts = {}
#
# for filename in filenames:
#     emotion_id = get_emotion_id(filename)
#     if emotion_id in counts:
#         counts[emotion_id] += 1
#     else:
#         counts[emotion_id] = 1
#
# for i in counts.items():
#     print(i)




os.environ['AWS_PROFILE'] = 'rackspaceAcc'

survey_repo = SurveyRepository("EmotionDataStack-dev-surveytable310F762D-1SADR68QRMPOO")
project_repo = ProjectRepository("EmotionDataStack-dev-projecttable27032958-GVCRDU4JG31B")

project_name = "singletest"

survey_response_items = survey_repo.get_surveys(project_name, generate_meta=False)
project_response_item = project_repo.get_project(project_name, generate_meta=False)

project_model = ProjectModel(**project_response_item)

filenames, emotion_ids = sample_filenames(survey_response_items,
                                          project_model,
                                          None)


print(filenames)
counts = {}
for filename in filenames:
    emotion_id = get_emotion_id(filename)
    if emotion_id in counts:
        counts[emotion_id] += 1
    else:
        counts[emotion_id] = 1

for i in counts.items():
    print(i)