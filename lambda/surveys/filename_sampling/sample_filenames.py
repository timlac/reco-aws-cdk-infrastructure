from enum import Enum
from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.emotion_id_sampling import get_emotion_ids_subset
from surveys.filename_sampling.balanced_filename_sampling import get_filenames_for_emotions
from surveys.filename_sampling.randomized_sampling import get_randomized_filenames

from utils import get_emotion_id, get_valence


class ValenceParameters(Enum):
    POSITIVE = "pos"
    NEGATIVE = "neg"
    ALL = "all"


def is_valid_valence(value):
    return any(value == valence.value for valence in ValenceParameters)


def filter_filenames(filenames, target_valence):
    ret = []
    for filename in filenames:
        valence = get_valence(filename)
        if valence == target_valence or valence == "neu":
            ret.append(filename)
    return ret


def filter_on_valence(filenames, valence_parameter):

    print(valence_parameter)

    if valence_parameter == ValenceParameters.ALL.value:
        return filenames
    elif valence_parameter == ValenceParameters.POSITIVE.value:
        return filter_filenames(filenames, valence_parameter)
    elif valence_parameter == ValenceParameters.NEGATIVE.value:
        return filter_filenames(filenames, valence_parameter)
    else:
        raise ValueError("Something went wrong with filter on valence, invalid valence parameter")


def sample_filenames(surveys, project_meta, valence_parameter):

    filenames = filter_on_valence(project_meta.s3_experiment_objects, valence_parameter)

    freq2filename = generate_frequency_2_filename(surveys, filenames)

    if project_meta.emotion_sampling_enabled:
        all_emotion_ids = [get_emotion_id(filename) for filename in filenames]

        emotion_ids = list(set(all_emotion_ids))

        if len(emotion_ids) > project_meta.emotions_per_survey:

            emotion_ids = get_emotion_ids_subset(freq2filename,
                                                 project_meta.emotions_per_survey)

        filenames = get_filenames_for_emotions(freq2filename,
                                               emotion_ids,
                                               project_meta.samples_per_survey)
    else:
        filenames = get_randomized_filenames(freq2filename,
                                             project_meta.samples_per_survey)
        emotion_ids = []

    return filenames, emotion_ids


