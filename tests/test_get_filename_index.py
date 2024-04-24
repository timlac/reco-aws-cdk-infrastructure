import json

path = "data/big_project/surveys.json"
with open(path) as json_data:
    surveys = json.load(json_data)
    survey = surveys[0]
    survey_items = survey.get("survey_items")

print(survey_items[50])
