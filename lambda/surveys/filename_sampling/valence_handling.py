from constants import Valences
from utils import get_valence


def is_valid_valence(value):
    return any(value == valence.value for valence in Valences)


def filter_filenames(filenames, target_valence):
    ret = []
    for filename in filenames:
        valence = get_valence(filename)
        if valence == target_valence or valence == Valences.NEUTRAL:
            ret.append(filename)
    return ret


def filter_on_valence(filenames, valence_parameter):
    if not valence_parameter:
        return filenames
    elif valence_parameter == Valences.POSITIVE.value:
        return filter_filenames(filenames, valence_parameter)
    elif valence_parameter == Valences.NEGATIVE.value:
        return filter_filenames(filenames, valence_parameter)
    else:
        raise ValueError("Something went wrong with filter on valence, invalid valence parameter: {}"
                         .format(valence_parameter))
