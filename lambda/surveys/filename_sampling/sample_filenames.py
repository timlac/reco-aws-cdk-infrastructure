from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.balanced_sampling.emotion_id_sampling import get_emotion_ids_subset
from surveys.filename_sampling.balanced_sampling.balanced_filename_sampling import balanced_filename_sampling
from surveys.filename_sampling.randomized_sampling import get_randomized_filenames
from surveys.filename_sampling.valence_handling import filter_on_valence

from utils import get_emotion_id


def sample_filenames(surveys, project_model, valence_parameter):
    filenames = filter_on_valence(project_model.s3_experiment_objects, valence_parameter)

    freq2filename = generate_frequency_2_filename(surveys, filenames)


    if project_model.balanced_sampling_enabled:
        # invoke balanced sampling method
        all_emotion_ids = [get_emotion_id(filename) for filename in filenames]
        emotion_ids = list(set(all_emotion_ids))

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
        emotion_ids = []

    return filenames, emotion_ids
