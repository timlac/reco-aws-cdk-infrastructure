from surveys.database.survey_model import SurveyModel
from utils import get_metadata


def survey_item_has_reply(has_reply):
    if has_reply == 1:
        return True
    elif has_reply == 0:
        return False
    else:
        raise Exception("Error: Something went wrong, has_reply is {}".format(has_reply))


def get_filename_index(survey_items, filename):
    """
    :param survey_items: a survey object
    :param filename:
    :return:
    """
    filename_idx = None
    for idx, survey_item in enumerate(survey_items):
        if survey_item.filename == filename:
            if survey_item_has_reply(survey_item.has_reply):
                raise Exception("Error: Reply already exists on user survey_item.")
            filename_idx = idx

    if filename_idx is None:
        raise Exception("Error: Filename {} not found...".format(filename))

    return filename_idx


def set_progress(surveys):
    for survey in surveys:
        count = sum(1 for item in survey.survey_items if item.has_reply == 1)
        total = len(survey.survey_items)
        survey.progress = count / total


def set_total_time_spent(surveys):
    for survey in surveys:
        MAX_TIME_SPENT_MS = 80000  # 80 seconds in milliseconds

        valid_items = [
            item for item in survey.survey_items
            if item.has_reply == 1 and item.time_spent_on_item is not None
        ]

        capped_times = [min(item.time_spent_on_item, MAX_TIME_SPENT_MS) for item in valid_items]

        survey.total_time_spent = sum(capped_times)


def generate_meta_for_survey(survey: SurveyModel):
    for survey_item in survey.survey_items:
        metadata = get_metadata(survey_item.filename)
        survey_item.metadata = metadata

