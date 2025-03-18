import os
import time
from collections import defaultdict
from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY
from surveys.database.survey_model import SurveyModel
from utils import generate_response, get_emotion_id
from surveys.database.survey_repository import SurveyRepository
from surveys.database.survey_item_utils import set_progress


def get_reply_stats(survey_models):
    """Computes item and emotion reply counts."""
    start_time = time.time()

    item_reply_count = defaultdict(int)
    emotion_reply_count = defaultdict(int)

    for survey in survey_models:
        for item in survey.survey_items:
            if item.has_reply:
                item_reply_count[item.filename] += 1
                emotion_id = get_emotion_id(item.filename)  # 🚨 Possible slowdown
                emotion_reply_count[emotion_id] += 1

    elapsed_time = time.time() - start_time
    print(f"[DEBUG] get_reply_stats execution time: {elapsed_time:.4f} sec")

    return dict(item_reply_count), dict(emotion_reply_count)


def handler(event, context):
    start_time = time.time()
    project_name = event['pathParameters'][PROJECT_NAME_KEY]

    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])

    # 🚀 Measure DynamoDB query time
    fetch_start = time.time()
    response_items = survey_repo.get_surveys(project_name, generate_meta=False)
    fetch_elapsed = time.time() - fetch_start
    print(f"[DEBUG] DynamoDB query time: {fetch_elapsed:.4f} sec")

    # 🚀 Measure model instantiation time
    model_start = time.time()
    survey_models = [SurveyModel(**item) for item in response_items]
    model_elapsed = time.time() - model_start
    print(f"[DEBUG] SurveyModel instantiation time: {model_elapsed:.4f} sec")

    # 🚀 Measure stats computation time
    stats_start = time.time()
    item_reply_count, emotion_reply_count = get_reply_stats(survey_models)
    stats_elapsed = time.time() - stats_start
    print(f"[DEBUG] get_reply_stats execution time: {stats_elapsed:.4f} sec")

    # 🚀 Measure total execution time
    total_elapsed = time.time() - start_time
    print(f"[DEBUG] Total execution time: {total_elapsed:.4f} sec")

    return generate_response(200, {
        "item_reply_count": item_reply_count,
        "emotion_reply_count": emotion_reply_count
    })
