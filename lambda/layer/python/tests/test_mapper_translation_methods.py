import unittest
from nexa_py_sentimotion_mapper.sentimotion_mapper import Mapper


class TestMapperTranslationMethods(unittest.TestCase):

    def test_get_emotion_abr_from_emotion(self):
        result = Mapper.get_emotion_abr_from_emotion("anger")
        self.assertEqual(result, "ang")

    def test_get_emotion_from_emotion_abr(self):
        result = Mapper.get_emotion_from_emotion_abr("ang")
        self.assertEqual(result, "anger")

    def test_get_emotion_id_from_emotion(self):
        result = Mapper.get_emotion_id_from_emotion("anger")
        self.assertEqual(result, 12)

    def test_get_emotion_from_id(self):
        result = Mapper.get_emotion_from_id(12)
        self.assertEqual(result, "anger")

    def test_get_emotion_abr_from_id(self):
        result = Mapper.get_emotion_abr_from_emotion_id(12)
        self.assertEqual(result, "ang")

    def test_get_id_from_emotion_abr(self):
        result = Mapper.get_id_from_emotion_abr("ang")
        self.assertEqual(result, 12)

    def test_get_valence_from_emotion(self):
        result = Mapper.get_valence_from_emotion("anger")
        self.assertEqual(result, "neg")

    def test_get_swe_translation_from_eng(self):
        result = Mapper.get_swe_translation_from_eng("anger")
        self.assertEqual(result, "ilska")

    def test_get_eng_translation_from_swe(self):
        result = Mapper.get_eng_translation_from_swe("ilska")
        self.assertEqual(result, "anger")


if __name__ == '__main__':
    unittest.main()

