import os



from constants import PROJECT_NAME_KEY, TABLE_NAME_KEY
from surveys.database.survey_model import SurveyModel
from utils import generate_response
from surveys.database.survey_repository import SurveyRepository
from surveys.database.survey_item_utils import set_progress, set_total_time_spent



def handler(event, context):
    project_name = event['pathParameters'][PROJECT_NAME_KEY]
    query_params = event.get("queryStringParameters", {}) or {}
    include_items = query_params.get("includeItems", "false").lower() == "true"

    survey_repo = SurveyRepository(os.environ[TABLE_NAME_KEY])

    try:
        response_items = survey_repo.get_surveys(project_name)
        survey_models = [SurveyModel(**item) for item in response_items]
        set_progress(survey_models)
        set_total_time_spent(survey_models)

        if include_items:
            ret = [survey.model_dump() for survey in survey_models]
            return generate_response(200, ret, compressed=True)  # ✅ Compressed response
        else:
            ret = [survey.dump_without_items() for survey in survey_models]
            return generate_response(200, ret)  # ✅ Normal JSON response

    except Exception as e:
        print(e)
        return generate_response(500, str(e))

