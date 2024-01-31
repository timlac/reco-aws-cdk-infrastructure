import json

from surveys.survey_item_handler import get_filename_index


path = "data/survey_items.json"
with open(path) as json_data:
    data = json.load(json_data)

print(data[343])
