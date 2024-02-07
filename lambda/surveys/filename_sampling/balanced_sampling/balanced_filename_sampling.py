import json
import math
import random
from utils import get_emotion_id


def prefilter_by_emotion(freq2filename):
    """
    Organize filenames by emotion ID for faster access.

    :param freq2filename: dict with keys: frequency and values: list of filenames
    :return: dict with keys: emotion_id and values: list of filenames sorted by frequency
    """
    frequencies = sorted(freq2filename.keys())

    emotion2filenames = {}
    for freq in frequencies:
        for filename in freq2filename[freq]:
            emotion_id = int(get_emotion_id(filename))

            emotion2filenames.setdefault(emotion_id, []).append(filename)

    return emotion2filenames


def get_files_with_emotion_2(emotion2filenames, emotion_id, count):
    """
    Sample filenames with a specific emotion id, prioritizing lower frequencies.

    :param emotion2filenames: dict with keys: emotion_id and values: list of filenames sorted by frequency
    :param emotion_id: emotion id to sample from
    :param count: number of files to generate
    :return: list of filenames
    """

    if emotion_id in emotion2filenames:
        return emotion2filenames[emotion_id][:count]
    else:
        return []


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

    emotion2filenames = prefilter_by_emotion(freq2filename)


    for emotion_id in emotion_ids:
        count = samples_per_emotion

        if emotion_id == emotion_ids[-1]:
            count = total_count - samples_collected

        filenames = get_files_with_emotion_2(emotion2filenames, emotion_id, count)
        ret.extend(filenames)
        samples_collected += len(filenames)

    random.shuffle(ret)
    return ret



path = "../../../../tests/data/project_data.json"

with open(path) as json_data:
    project_data = json.load(json_data)
    json_data.close()

from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
import math
from collections import Counter
import time
from collections import Counter


f2f = generate_frequency_2_filename([], project_data["s3_experiment_objects"])
eis = [get_emotion_id(filename) for filename in project_data["s3_experiment_objects"]]

eis = list(set(eis))

start = time.time()
ret = get_filenames_for_emotions(f2f, eis, 110)
end = time.time()

print("elasped time: ", end - start)


final_emotion_ids = [get_emotion_id(filename) for filename in ret]

print(final_emotion_ids)

counts = Counter(final_emotion_ids)

print(counts)


