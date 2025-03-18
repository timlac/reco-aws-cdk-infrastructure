
"""
Would like to get the following stats:
- Dict with key: item and value: number of replies
- Dict with key: emotion and value: number of replies
"""
import time

import os
from collections import defaultdict

from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY
from surveys.database.survey_model import SurveyModel
from utils import generate_response, get_emotion_id
from surveys.database.survey_repository import SurveyRepository
from surveys.database.survey_item_utils import set_progress


def get_reply_stats(survey_models):
    """
    Returns:
        - Dict with key: item filename and value: number of replies
        - Dict with key: emotion_id and value: number of replies
    """

    start_time = time.time()


    item_reply_count = defaultdict(int)
    emotion_reply_count = defaultdict(int)

    for survey in survey_models:
        for item in survey.survey_items:
            if item.has_reply:
                # Count replies per item
                item_reply_count[item.filename] += 1

                emotion_id = get_emotion_id(item.filename)
                emotion_reply_count[emotion_id] += 1

    elapsed_time = time.time() - start_time
    print(f"[DEBUG] get_reply_stats execution time: {elapsed_time:.4f} sec")

    return dict(item_reply_count), dict(emotion_reply_count)


def handler(event, context):
    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])

    try:
        response_items = survey_repo.get_surveys(project_name)

        # setting the progress variable
        survey_models = [SurveyModel(**item) for item in response_items]
        item_reply_count, emotion_reply_count = get_reply_stats(survey_models)

        ret = {
            "item_reply_count": item_reply_count,
            "emotion_reply_count": emotion_reply_count
        }

        return generate_response(200, ret)

    except Exception as e:
        print(e)
        return generate_response(500, str(e))
