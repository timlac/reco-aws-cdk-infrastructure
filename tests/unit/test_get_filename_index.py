import unittest
import json

# Assuming your function and any dependencies (like survey_item_has_reply) are defined in a file named 'survey_utils.py'
from surveys.survey_item_handler import get_filename_index, survey_item_has_reply


class TestGetFilenameIndex(unittest.TestCase):

    def setUp(self):
        # Setup mock survey items
        path = "../data/survey_items.json"
        with open(path) as json_data:
            self.survey_items = json.load(json_data)

    def test_get_filename_index_success(self):
        # Test finding an index successfully
        filename = 'A221_hap_p_3.mp4'
        expected_index = 343
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
        filename = 'A75_anx_p_2.mp4'
        with self.assertRaises(Exception) as context:
            get_filename_index(self.survey_items, filename)
        self.assertTrue('Reply already exists on user survey_item.' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
