from utils import get_valence


def get_filename(survey_item, survey_id):
    filename = survey_item.get("filename")
    if filename is None:
        raise KeyError("The key 'filename' was not found in the survey_item {} in survey {}"
                       .format(survey_item, survey_id))
    else:
        return filename


def invert(filename2freq):
    ret = {}
    for filename, frequency in filename2freq.items():
        if frequency in ret:
            ret[frequency].append(filename)
        else:
            ret[frequency] = [filename]
    return ret


def generate_frequency_2_filename(surveys, filenames):
    filename2freq = {}
    for filename in filenames:
        filename2freq[filename] = 0

    for survey in surveys:
        survey_id = survey.get("survey_id")

        for survey_item in survey.get("survey_items", []):
            filename = get_filename(survey_item, survey_id)

            if filename in filename2freq:
                filename2freq[filename] += 1

    freq2filename = invert(filename2freq)

    return freq2filename

