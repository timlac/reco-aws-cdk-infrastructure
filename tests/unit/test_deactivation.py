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
import datetime
from zoneinfo import ZoneInfo


class TestSamplingSmallProject(unittest.TestCase):

    def setUp(self):
        # Setup mock survey items
        project_path = "../data/expire_project/project.json"
        with open(project_path) as json_data:
            project = json.load(json_data)
            self.project_model = ProjectModel(**project)

        surveys_path = "../data/expire_project/surveys.json"
        with open(surveys_path) as json_data:
            surveys = json.load(json_data)
            self.survey_models = [SurveyModel(**data) for data in surveys]

    def sample_emotions(self):
        emotion_ids = []
        for survey in self.survey_models:
            for survey_item in survey.survey_items:
                meta = survey_item.metadata
                emotion_id = meta.get('emotion_1_id')
                emotion_ids.append(emotion_id)

        existing_emotion_ids = set(emotion_ids)

        filenames, emo_ids = sample_filenames(self.survey_models, self.project_model, None)
        print(filenames)

        output_emotion_ids = set([get_emotion_id(filename) for filename in filenames])
        print(existing_emotion_ids)
        print(output_emotion_ids)

        return existing_emotion_ids, output_emotion_ids

    def test_sample_with_and_without_deactivation(self):
        # first we sample emotions when there is no setting for days to deactivation
        existing_emotion_ids, output_emotion_ids = self.sample_emotions()
        # since existing surveys will be taken into account when sampling new filenames
        # there should be no overlap in sampled filenames
        assert existing_emotion_ids.isdisjoint(output_emotion_ids)

        # we set days to deactivation to seven, and since the survey is created more than 7 days ago,
        # and is not finished
        # it should not be taken into account when sampling new filenames
        self.project_model.days_to_deactivation = 7

        # we sample again and assert that there is overlap,
        # the probability that there is no overlap is in this case very small
        existing_emotion_ids, output_emotion_ids = self.sample_emotions()
        assert existing_emotion_ids.intersection(output_emotion_ids)

        # now we change the date of last modified
        self.survey_models[0].last_modified = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        existing_emotion_ids, output_emotion_ids = self.sample_emotions()
        assert existing_emotion_ids.isdisjoint(output_emotion_ids)

        # we remove it again
        self.survey_models[0].last_modified = None

        # finish the survey...
        for survey in self.survey_models:
            for survey_item in survey.survey_items:
                survey_item.has_reply = 1

        # now the sampled filenames should be disjoint again...
        existing_emotion_ids, output_emotion_ids = self.sample_emotions()
        assert existing_emotion_ids.isdisjoint(output_emotion_ids)


if __name__ == '__main__':
    unittest.main()
