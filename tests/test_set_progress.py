import json

from surveys.database.survey_model import SurveyModel


def set_progress(surveys):
    for survey in surveys:

        count = sum(1 for item in survey.survey_items if item.has_reply == 1)
        total = len(survey.survey_items)
        survey.progress = count / total


path = "data/surveys.json"
with open(path) as json_data:
    data = json.load(json_data)

    survey_models = [SurveyModel(**d) for d in data]

    for i in survey_models:
        print(i.dict())

    ret = [survey.dict() for survey in survey_models]
    print()
    for i in ret:
        print(i)

