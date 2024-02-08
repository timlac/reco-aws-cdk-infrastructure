

def initialize_survey_item(survey_item):
    survey_item["reply"] = survey_item.get("reply", [])
    survey_item["has_reply"] = survey_item.get("has_reply", 0)
    return survey_item


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


def set_progress(survey_items):
    for idx, survey in enumerate(survey_items):
        count = sum(1 for item in survey["survey_items"] if item["has_reply"] == 1)
        total = len(survey["survey_items"])

        survey_items[idx]["progress"] = count / total
    return survey_items
