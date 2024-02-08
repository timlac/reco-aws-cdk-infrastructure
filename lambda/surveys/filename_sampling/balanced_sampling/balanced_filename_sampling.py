
import json
import math
from collections import Counter

import random
from utils import get_emotion_id


def prefilter_by_emotion(freq2filename, skip):
    """
    Organize filenames by emotion ID for faster access.

    :param freq2filename: dict with keys: frequency and values: list of filenames
    :return: dict with keys: emotion_id and values: list of filenames sorted by frequency
    """
    frequencies = sorted(freq2filename.keys())

    emotion2filenames = {}
    for freq in frequencies:
        filenames = freq2filename[freq]
        random.shuffle(filenames)

        for filename in filenames:
            if filename not in skip:
                emotion_id = int(get_emotion_id(filename))
                emotion2filenames.setdefault(emotion_id, []).append(filename)

    return emotion2filenames


def adjust_samples_per_emotion(filenames, total_samples):
    emotions = [get_emotion_id(filename) for filename in filenames]

    # Get the distribution of emotion IDs
    emotion_distribution = Counter(emotions)

    # Calculate the total number of samples in the dataset
    total_count = sum(emotion_distribution.values())

    # Calculate samples per emotion based on its proportion in the dataset
    samples_per_emotion = {}
    for emotion_id, count in emotion_distribution.items():
        proportion = count / total_count
        samples_per_emotion[emotion_id] = math.floor(total_samples * proportion)

    return samples_per_emotion


def get_x_number_of_files_per_emotion(emotion2filenames, samples_per_emotion, break_on):
    """
    Sample filenames with a specific emotion id, prioritizing lower frequencies.

    :param emotion2filenames: dict with keys: emotion_id and values: list of filenames sorted by frequency
    :param samples_per_emotion: number of files to generate
    :param break_on: break when we reach this number
    :return: list of filenames
    """
    ret = []
    for idx, emotion_id in enumerate(samples_per_emotion.keys()):
        if emotion_id in emotion2filenames:
            number_of_samples = samples_per_emotion[emotion_id]
            filenames = emotion2filenames[emotion_id][:number_of_samples]
            ret.extend(filenames)

            # Adjusted to break_on - 1 since idx starts from 0
            if idx >= break_on - 1:
                return ret

    return ret


def filter_filenames(freq2filename, emotion_ids):
    all_filenames = sum(freq2filename.values(), [])

    filtered_filenames = []
    for filename in all_filenames:
        emotion_id = get_emotion_id(filename)
        if emotion_id in emotion_ids:
            filtered_filenames.append(filename)
    return filtered_filenames


def balanced_filename_sampling(freq2filename, emotion_ids, total_count):
    """
    This function generates a balanced list of filenames for specified emotion ids

    :param freq2filename: dict with keys: frequency and values: list of filenames
    :param emotion_ids: emotion ids to sample from
    :param total_count: total number of filenames to generate
    :return:
    """
    ret = []

    filtered_filenames = filter_filenames(freq2filename, emotion_ids)
    emotion2filenames = prefilter_by_emotion(freq2filename, set())

    samples_per_emotion = adjust_samples_per_emotion(filtered_filenames, total_count)

    sampled_filenames = get_x_number_of_files_per_emotion(emotion2filenames,
                                                          samples_per_emotion,
                                                          total_count)
    ret.extend(sampled_filenames)

    # this introduces an element of chance, so the results will not be the same every time this function is run
    # filenames corresponding to the first emotions in the emotion_ids list will be sampled while the last ones will not
    random.shuffle(emotion_ids)
    samples_per_emotion = {}
    for emotion_id in emotion_ids:
        samples_per_emotion[emotion_id] = 1

    remaining_count = total_count - len(sampled_filenames)

    emotion2filenames = prefilter_by_emotion(freq2filename, set(sampled_filenames))
    filler_filenames = get_x_number_of_files_per_emotion(emotion2filenames,
                                                         samples_per_emotion,
                                                         remaining_count)
    ret.extend(filler_filenames)

    random.shuffle(ret)
    return ret
