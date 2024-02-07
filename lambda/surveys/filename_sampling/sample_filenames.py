from projects import project_model
from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.balanced_sampling.emotion_id_sampling import get_emotion_ids_subset
from surveys.filename_sampling.balanced_sampling.balanced_filename_sampling import get_filenames_for_emotions
from surveys.filename_sampling.randomized_sampling import get_randomized_filenames
from surveys.filename_sampling.valence_handling import filter_on_valence

from utils import get_emotion_id

from collections import Counter
import math
import json


def adjust_samples_per_emotion(filenames, total_samples):
    # Get the emotion IDs for each filename
    emotions = [get_emotion_id(filename) for filename in filenames]

    # Get the distribution of emotion IDs
    emotion_distribution = Counter(emotions)

    print(emotion_distribution)

    # Calculate the total number of samples in the dataset
    total_count = sum(emotion_distribution.values())

    print(total_count)

    # Calculate samples per emotion based on its proportion in the dataset
    samples_per_emotion = {}
    for emotion_id, count in emotion_distribution.items():
        proportion = count / total_count
        samples_per_emotion[emotion_id] = math.floor(total_samples * proportion)

    return samples_per_emotion


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

        filenames = get_filenames_for_emotions(freq2filename,
                                               emotion_ids,
                                               project_model.samples_per_survey)
    else:
        # invoke randomized sampling method
        filenames = get_randomized_filenames(freq2filename,
                                             project_model.samples_per_survey)
        emotion_ids = []

    return filenames, emotion_ids


path = "../../../tests/data/project_data.json"

with open("../../../tests/data/project_data.json") as json_data:
    d = json.load(json_data)
    json_data.close()

print(type(d["samples_per_survey"]))

samples_per_emotion = adjust_samples_per_emotion(d["s3_experiment_objects"], int(d["samples_per_survey"]))
for i in samples_per_emotion.items():
    print(i)

print(sum(samples_per_emotion.values()))