import statistics
import unittest
import json
from collections import Counter

from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.balanced_sampling.balanced_filename_sampling import balanced_filename_sampling
from utils import get_emotion_id


class TestBalancedFilenameSampling(unittest.TestCase):

    def setUp(self):
        # Setup mock survey items
        path = "../data/big_project/project.json"
        with open(path) as json_data:
            project_data = json.load(json_data)
            self.frequency2filename = generate_frequency_2_filename([], project_data["s3_experiment_objects"])

    def test_sampling_equally_distributed_filenames(self):
        emotion_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        samples_per_survey = 132

        filenames = balanced_filename_sampling(self.frequency2filename, emotion_ids, samples_per_survey)
        output_emotion_ids = [get_emotion_id(filename) for filename in filenames]
        counts = Counter(output_emotion_ids)
        print("counts: ", counts)
        # Extract the counts from the Counter object
        values = list(counts.values())
        # Calculate the standard deviation
        std_dev = statistics.stdev(values)
        print("std_dev: ", std_dev)

        self.assertLess(std_dev, 1, "The standard deviation should be below 2 for a fairly equal distribution")

        output_emotion_ids = list(set(output_emotion_ids))

        self.assertEqual(len(filenames), samples_per_survey)
        self.assertEqual(len(emotion_ids), len(output_emotion_ids))
        self.assertEqual(set(emotion_ids), set(output_emotion_ids))


if __name__ == '__main__':
    unittest.main()
