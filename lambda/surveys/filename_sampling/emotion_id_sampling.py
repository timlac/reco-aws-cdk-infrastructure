import random

from utils import get_emotion_id


def get_emotion_ids_subset(freq2filename, subset_size):
    """
    This function samples emotion ids from the lowest frequencies in freq2filename

    :param freq2filename: dict with keys: frequency and values: list of filenames
    :param subset_size: desired size
    :return: list of emotion ids
    """
    frequencies = sorted(freq2filename.keys(), key=int)
    collected_emotion_ids = set()

    for freq in frequencies:
        filenames = freq2filename[freq]
        emotion_ids = [get_emotion_id(filename) for filename in filenames]
        unique_emotion_ids = set(emotion_ids)

        # check if collected plus new is less than or equal to count
        if len(collected_emotion_ids) + len(unique_emotion_ids) <= subset_size:
            # simply update collected emotion ids
            collected_emotion_ids.update(unique_emotion_ids)
            if len(collected_emotion_ids) == subset_size:
                break
        else:
            # if collected plus new is more than count, then carefully sample from new emotion ids to fill up,
            # then break
            needed_ids = subset_size - len(collected_emotion_ids)
            additional_ids = random.sample(list(unique_emotion_ids), needed_ids)
            collected_emotion_ids.update(set(additional_ids))
            break  # We've reached the desired count, so we can exit the loop

    return list(collected_emotion_ids)
