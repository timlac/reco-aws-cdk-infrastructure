from enum import Enum

PROJECT_NAME_KEY = 'project_name'
SURVEY_ID_KEY = 'survey_id'
TABLE_NAME_KEY = 'DYNAMODB_TABLE_NAME'


class Valences(Enum):
    POSITIVE = "pos"
    NEGATIVE = "neg"
    NEUTRAL = "neu"
