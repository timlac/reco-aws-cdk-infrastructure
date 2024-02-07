import json

path = "data/survey_items.json"
with open(path) as json_data:
    data = json.load(json_data)

print(data[343])
