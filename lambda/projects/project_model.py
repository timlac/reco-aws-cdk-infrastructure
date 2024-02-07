from pydantic import BaseModel
from typing import Dict, Any


class ProjectModel(BaseModel):
    project_name: str
    s3_experiment_objects: list[str]
    s3_intro_objects: list[str]
    s3_folder: str

    reply_format: Dict[str, Any]
    instructions: Dict[str, Any]

    samples_per_survey: int
    balanced_sampling_enabled: bool
    emotions_per_survey: int
