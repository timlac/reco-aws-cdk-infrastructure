import unittest
import json
from collections import Counter

from surveys.database.survey_model import SurveyModel
from utils import get_emotion_id, within_time_delta


class TestGetRandomizedFilenames(unittest.TestCase):

    def setUp(self):
        # Setup mock survey items
        project_path = "../data/small_project/project.json"
        with open(project_path) as json_data:
            self.project_data = json.load(json_data)

        surveys_path = "../data/small_project/surveys.json"
        with open(surveys_path) as json_data:
            self.surveys = json.load(json_data)

    def test_within(self):
        surveys = [SurveyModel(**data) for data in self.surveys]
        for survey in surveys:
            ret = within_time_delta(survey, 1)
            print(ret)


if __name__ == '__main__':
    unittest.main()
