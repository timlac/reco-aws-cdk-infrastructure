import random


def get_randomized_filenames(freq2filename, total_count):
    """
    This function generates a balanced list of filenames for specified emotion ids

    :param freq2filename: dict with keys: frequency and values: list of filenames
    :param total_count: total number of filenames to generate
    :return:
    """
    ret = []
    frequencies = sorted(freq2filename.keys())
    for freq in frequencies:
        filenames = freq2filename[freq]
        random.shuffle(filenames)

        for filename in filenames:
            if len(ret) < total_count:
                ret.append(filename)
            else:
                break

    random.shuffle(ret)
    return ret
