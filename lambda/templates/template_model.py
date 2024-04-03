from pydantic import BaseModel
from typing import Any, Optional, Dict


class TemplateModel(BaseModel):
    # partition key
    template_id: str
    # sort key
    template_type: str

    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    templateJson: Dict[str, Any]

