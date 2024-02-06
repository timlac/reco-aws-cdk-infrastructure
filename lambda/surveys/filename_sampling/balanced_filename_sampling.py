import json
import math
import random
from utils import get_emotion_id


def get_files_with_emotion(freq2filename, emotion_id, count):
    """
    This function samples filenames with a specific emotion id from the lowest frequencies in frequency 2 filename

    :param freq2filename: dict with keys: frequency and values: list of filenames
    :param emotion_id: emotion id to sample from
    :param count: number of files to generate
    :return: list of filenames
    """
    ret = []
    frequencies = sorted(freq2filename.keys())
    for freq in frequencies:
        for filename in freq2filename[freq]:
            if int(get_emotion_id(filename)) == emotion_id:
                if len(ret) < count:
                    ret.append(filename)
                else:
                    break
        if len(ret) >= count:
            break
    return ret


def get_filenames_for_emotions(freq2filename, emotion_ids, total_count):
    """
    This function generates a balanced list of filenames for specified emotion ids

    :param freq2filename: dict with keys: frequency and values: list of filenames
    :param emotion_ids: emotion ids to sample from
    :param total_count: total number of filenames to generate
    :return:
    """
    random.shuffle(emotion_ids)

    samples_per_emotion = math.floor(total_count / len(emotion_ids))
    samples_collected = 0
    ret = []

    for emotion_id in emotion_ids:
        count = samples_per_emotion

        if emotion_id == emotion_ids[-1]:
            count = total_count - samples_collected

        filenames = get_files_with_emotion(freq2filename, emotion_id, count)
        ret.extend(filenames)
        samples_collected += len(filenames)

    random.shuffle(ret)
    return ret


#
#
# with open('../../../tests/data/project_data.json') as f:
#     project_data = json.load(f)
#
# with open('../../../tests/data/survey_data.json') as f:
#     survey_data = json.load(f)
#
# freq_2_filename = generate_frequency_2_filename(survey_data, project_data['s3_experiment_objects'])
#
# # emotion_files = get_files_with_emotion(freq_2_filename, 34, 20)
# #
# # print(emotion_files)
# #
# # ids = [34, 38, 41]
# #
# # samples = get_filenames_for_emotions(freq_2_filename, ids, 10)
# #
# # print(samples)
# # print(len(samples))
#
#
# var = get_emotion_ids_subset(freq_2_filename, 5)
# print(var)
# print(len(var))