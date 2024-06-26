import statistics
import unittest
import json
from collections import Counter

from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.randomized_sampling import get_randomized_filenames
from utils import get_emotion_id


class TestGetRandomizedFilenames(unittest.TestCase):

    def setUp(self):
        print("setting up....")
        # Setup mock survey items
        project_path = "../data/big_project/project.json"
        with open(project_path) as json_data:
            self.project_data = json.load(json_data)

        surveys_path = "../data/big_project/surveys.json"
        with open(surveys_path) as json_data:
            self.surveys = json.load(json_data)

    def test_sample(self):
        freq2filename = generate_frequency_2_filename(self.surveys, self.project_data["s3_experiment_objects"])
        filenames = get_randomized_filenames(freq2filename, int(self.project_data["samples_per_survey"]))

        print(filenames)

        self.assertEqual(len(filenames), int(self.project_data["samples_per_survey"]))

    def test_sampling_equally_distributed_filenames(self):
        emotion_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        samples_per_survey = 132

        filtered_filenames = []
        for filename in self.project_data["s3_experiment_objects"]:
            if get_emotion_id(filename) in emotion_ids:
                filtered_filenames.append(filename)

        freq2filename = generate_frequency_2_filename([], filtered_filenames)

        filenames = get_randomized_filenames(freq2filename, samples_per_survey)
        output_emotion_ids = [get_emotion_id(filename) for filename in filenames]
        counts = Counter(output_emotion_ids)
        print("counts: ", counts)
        # Extract the counts from the Counter object
        values = list(counts.values())
        # Calculate the standard deviation
        std_dev = statistics.stdev(values)
        print("std_dev: ", std_dev)

        # self.assertLess(std_dev, 1, "The standard deviation should be below 2 for a fairly equal distribution")

        output_emotion_ids = list(set(output_emotion_ids))

        self.assertEqual(len(filenames), samples_per_survey)
        self.assertEqual(len(emotion_ids), len(output_emotion_ids))
        self.assertEqual(set(emotion_ids), set(output_emotion_ids))


if __name__ == '__main__':
    unittest.main()
