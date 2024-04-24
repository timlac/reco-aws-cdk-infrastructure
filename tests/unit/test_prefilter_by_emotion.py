import statistics
import unittest
import json
from collections import Counter

from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename, generate_filename2freq
from surveys.filename_sampling.balanced_sampling.balanced_filename_sampling import prefilter_by_emotion
from utils import get_emotion_id


class TestPrefilterByEmotion(unittest.TestCase):

    def setUp(self):
        project_data_path = "../data/big_project/project.json"
        with open(project_data_path) as json_data:
            project_data = json.load(json_data)

        surveys_path = "../data/big_project/surveys.json"
        with open(surveys_path) as json_data:
            survey_data = json.load(json_data)

        self.filename2frequency = generate_filename2freq(survey_data, project_data["s3_experiment_objects"])
        self.frequency2filename = generate_frequency_2_filename(survey_data, project_data["s3_experiment_objects"])

    def test_generate(self):
        emotion2filenames = prefilter_by_emotion(self.frequency2filename, set())

        emotion2filenames_length = sum(len(filenames) for filenames in emotion2filenames.values())
        filename2frequency_length = sum(len(filenames) for filenames in self.frequency2filename.values())

        self.assertEqual(emotion2filenames_length, filename2frequency_length)

        for emotion_id, filenames in emotion2filenames.items():
            highest_freq = -1
            for filename in filenames:
                freq = self.filename2frequency[filename]
                self.assertGreaterEqual(freq, highest_freq,
                                        f"File {filename} with freq {freq} is out of order in emotion {emotion_id}")

                if freq > highest_freq:
                    highest_freq = freq

    def test_skip(self):
        skip = [
            "A102_reg_v_3.mp4",
            "A102_ang_v_2.mp4",
            "A102_ang_v_3.mp4",
            "A102_anx_p_2.mp4",
            "A102_anx_p_3.mp4",
            "A102_anx_v_2.mp4",
            "A102_anx_v_3.mp4",
            "A102_awe_p_2.mp4",
            "A102_awe_p_3.mp4",
        ]

        emotion2filenames = prefilter_by_emotion(self.frequency2filename, set(skip))

        for emotion, filenames in emotion2filenames.items():
            for filename in filenames:
                self.assertNotIn(filename, skip, f"Filename {filename} should have been skipped for emotion {emotion}")


if __name__ == '__main__':
    unittest.main()
