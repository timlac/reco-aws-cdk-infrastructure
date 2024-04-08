from pydantic import BaseModel
from typing import Any, Optional, Dict
import datetime
from zoneinfo import ZoneInfo


class TemplateModel(BaseModel):
    # partition key
    template_name: str
    # sort key
    template_type: str

    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    template_json: Dict[str, Any]

    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        super().__init__(**data)

