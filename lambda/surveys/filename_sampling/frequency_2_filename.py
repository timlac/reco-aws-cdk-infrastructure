from surveys.database.survey_model import SurveyModel
from utils import within_time_delta


def invert(filename2freq):
    ret = {}
    for filename, frequency in filename2freq.items():
        if frequency in ret:
            ret[frequency].append(filename)
        else:
            ret[frequency] = [filename]
    return ret


def survey_is_finished(survey: SurveyModel):
    for survey_item in survey.survey_items:
        if survey_item.has_reply != 1:
            return False
    return True


def generate_filename2freq(surveys: list[SurveyModel], filenames: list, days_to_deactivation=None):
    """
    Generate a dictionary that maps filenames to frequencies.
    """

    filename2freq = {}
    for filename in filenames:
        filename2freq[filename] = 0

    for survey in surveys:

        # check if there is any days_to_deactivation parameter set
        if days_to_deactivation:
            # check if survey is created/modified recently enough to be considered active
            if not within_time_delta(survey, days_to_deactivation):
                # check if survey is unfinished
                if not survey_is_finished(survey):
                    # continue (skip) if:
                    # - days_to_deactivation is set
                    # - not within time delta
                    # - not finished
                    continue

        # iterate through survey items and add to filename 2 frequency dict
        for survey_item in survey.survey_items:
            filename = survey_item.filename

            if filename in filename2freq:
                filename2freq[filename] += 1
            else:
                raise ValueError("Survey item {} with filename {} "
                                 "was not found in list of filenames".format(survey_item, filename))

    return filename2freq


def generate_frequency_2_filename(surveys, filenames, days_to_deactivation=None):
    filename2freq = generate_filename2freq(surveys, filenames, days_to_deactivation)
    freq2filename = invert(filename2freq)
    return freq2filename

