from pydantic import BaseModel
from typing import Any, Optional, Dict

import datetime
from zoneinfo import ZoneInfo


class SurveyItemModel(BaseModel):
    filename: str
    has_reply: int
    reply: list[Any]
    time_spent_on_item: Optional[int] = None
    video_duration: Optional[int] = None
    last_modified: Optional[str] = None
    metadata: Dict[str, Any] = {}


class SurveyModel(BaseModel):
    # partition key
    project_name: str
    # sort key
    survey_id: str
    # metadata
    created_at: str
    user_id: str
    valence: Optional[str] = None
    date_of_birth: Optional[str] = None
    sex: Optional[str] = None
    consent: bool
    # the emotion alternatives included in the survey items
    emotion_ids: list[int]
    survey_items: list[SurveyItemModel]

    progress: Optional[float] = None
    last_modified: Optional[str] = None

    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        super().__init__(**data)
