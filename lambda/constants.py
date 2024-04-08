from enum import Enum

PROJECT_NAME_KEY = 'project_name'
SURVEY_ID_KEY = 'survey_id'
TEMPLATE_NAME_KEY = 'template_name'
TEMPLATE_TYPE_KEY = 'template_type'
TABLE_NAME_KEY = 'DYNAMODB_TABLE_NAME'


class Valences(Enum):
    POSITIVE = "pos"
    NEGATIVE = "neg"
    NEUTRAL = "neu"
