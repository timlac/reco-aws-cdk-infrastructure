import statistics
import unittest
import json
from collections import Counter

from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.balanced_sampling.balanced_filename_sampling import adjust_samples_per_emotion
from utils import get_emotion_id


class TestAdjustSamplesPerEmotion(unittest.TestCase):

    def setUp(self):
        # Setup mock survey items
        path = "../data/project_data.json"
        with open(path) as json_data:
            project_data = json.load(json_data)
            self.filenames = project_data["s3_experiment_objects"]

    def test_proportions_from_adjusted(self):
        id_1 = 22
        id_2 = 34

        # calculate proportions manually
        example_files_1 = [filename for filename in self.filenames if get_emotion_id(filename) == id_1]
        example_files_2 = [filename for filename in self.filenames if get_emotion_id(filename) == id_2]
        proportion_example_1_and_2 = len(example_files_1) / len(example_files_2)

        samples_per_survey = 200
        samples_per_emotion = adjust_samples_per_emotion(self.filenames, samples_per_survey)
        proportions_from_adjusted = samples_per_emotion[id_1] / samples_per_emotion[id_2]

        # Check if the absolute difference between the numbers is less than or equal to 1
        self.assertTrue(abs(proportion_example_1_and_2 - proportions_from_adjusted) <= 1,
                        "The proportions are not within the allowed difference of 1")


if __name__ == '__main__':
    unittest.main()
