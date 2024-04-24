import unittest
import json

from surveys.database.survey_item_handler import get_filename_index
from surveys.database.survey_model import SurveyItemModel


class TestGetFilenameIndex(unittest.TestCase):

    def setUp(self):
        # Setup mock survey items
        path = "../data/big_project/surveys.json"
        with open(path) as json_data:
            surveys = json.load(json_data)
            survey = surveys[0]
            self.survey_items = []
            for survey_item in survey.get("survey_items"):
                self.survey_items.append(SurveyItemModel(**survey_item))

    def test_get_filename_index_success(self):
        # Test finding an index successfully
        filename = 'A102_gra_v_2.mp4'
        expected_index = 2
        result = get_filename_index(self.survey_items, filename)
        self.assertEqual(result, expected_index)

    def test_filename_not_found(self):
        # Test the exception when filename is not found
        filename = 'non_existent_file.txt'
        with self.assertRaises(Exception) as context:
            get_filename_index(self.survey_items, filename)
        self.assertTrue('Filename {} not found...'.format(filename) in str(context.exception))

    def test_filename_with_reply(self):
        # Test the exception when the survey item already has a reply
        filename = 'A102_reg_v_3.mp4'
        with self.assertRaises(Exception) as context:
            get_filename_index(self.survey_items, filename)
        self.assertTrue('Reply already exists on user survey_item.' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
