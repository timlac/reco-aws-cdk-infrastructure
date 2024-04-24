import statistics
import unittest
import json
from collections import Counter

from surveys.database.survey_model import SurveyModel
from surveys.filename_sampling.frequency_2_filename import generate_frequency_2_filename
from surveys.filename_sampling.randomized_sampling import get_randomized_filenames
from surveys.filename_sampling.sample_filenames import sample_filenames
from projects.project_model import ProjectModel
from utils import get_emotion_id


class TestSamplingSmallProject(unittest.TestCase):

    def setUp(self):
        # Setup mock survey items
        project_path = "../data/small_project/project.json"
        with open(project_path) as json_data:
            self.project_data = json.load(json_data)

        surveys_path = "../data/small_project/surveys.json"
        with open(surveys_path) as json_data:
            self.surveys = json.load(json_data)

    def test_sample(self):
        surveys = [SurveyModel(**data) for data in self.surveys]

        freq2filename = generate_frequency_2_filename(surveys, self.project_data["s3_experiment_objects"])
        filenames = get_randomized_filenames(freq2filename, int(self.project_data["samples_per_survey"]))

        print(filenames)

        self.assertEqual(len(filenames), int(self.project_data["samples_per_survey"]))

    def test_sampled_emotions(self):
        emotion_ids = []
        for survey in self.surveys:
            for survey_item in survey.get("survey_items"):
                meta = survey_item.get("metadata")
                emotion_id = meta.get("emotion_1_id")
                emotion_ids.append(emotion_id)

        existing_emotion_ids = set(emotion_ids)

        project_model = ProjectModel(**self.project_data)
        surveys = [SurveyModel(**data) for data in self.surveys]

        filenames, emo_ids = sample_filenames(surveys, project_model, None)
        print(filenames)

        output_emotion_ids = set([get_emotion_id(filename) for filename in filenames])
        print(existing_emotion_ids)
        print(output_emotion_ids)

        assert existing_emotion_ids.isdisjoint(output_emotion_ids)


if __name__ == '__main__':
    unittest.main()
