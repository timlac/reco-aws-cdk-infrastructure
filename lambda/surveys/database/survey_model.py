from pydantic import BaseModel
from typing import Any

import datetime
from zoneinfo import ZoneInfo


class SurveyItemModel(BaseModel):
    filename: str
    has_reply: int
    reply: list[Any]


class SurveyModel(BaseModel):
    # partition key
    project_name: str
    # sort key
    survey_id: str
    # metadata
    created_at: str
    user_id: str
    valence: str
    date_of_birth: str
    sex: str
    # the emotion alternatives included in the survey items
    emotion_alternatives: list[int]
    survey_items: list[SurveyItemModel]

    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        super().__init__(**data)
