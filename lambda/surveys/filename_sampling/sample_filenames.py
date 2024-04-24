from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.balanced_sampling.emotion_id_sampling import get_emotion_ids_subset
from surveys.filename_sampling.balanced_sampling.balanced_filename_sampling import balanced_filename_sampling
from surveys.filename_sampling.randomized_sampling import get_randomized_filenames
from surveys.filename_sampling.valence_handling import filter_on_valence

from utils import get_emotion_id


def sample_filenames(surveys, project_model, valence_parameter):
    """
    :param surveys: list with all surveys
    :param project_model: project model with metadata, such as all existing filenames to sample from
    :param valence_parameter: if None use all filenames, if pos or neg use only subset of filenames
    """

    # get all available filenames
    filenames = filter_on_valence(project_model.s3_experiment_objects, valence_parameter)

    # TODO: introduce a positive parameter in survey called active, or a negative parameter called archived
    # TODO: use this parameter to exclude inactive/archived surveys from this step

    # generate frequency 2 filename, a dict that describes how often filenames occur in existing surveys.
    freq2filename = generate_frequency_2_filename(surveys, filenames, project_model.days_to_deactivation)

    # get all emotion ids in filenames as list
    all_emotion_ids = [get_emotion_id(filename) for filename in filenames]
    emotion_ids = list(set(all_emotion_ids))

    if project_model.balanced_sampling_enabled:
        # invoke balanced sampling method

        if len(emotion_ids) > project_model.emotions_per_survey:
            # sample limited number of filenames from all available
            emotion_ids = get_emotion_ids_subset(freq2filename,
                                                 project_model.emotions_per_survey)

        filenames = balanced_filename_sampling(freq2filename,
                                               emotion_ids,
                                               project_model.samples_per_survey)
    else:
        # invoke randomized sampling method
        filenames = get_randomized_filenames(freq2filename,
                                             project_model.samples_per_survey)

    return filenames, emotion_ids
