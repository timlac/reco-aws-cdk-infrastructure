# mapper.py
import numpy as np
import json
import os
from pkg_resources import resource_filename


class Mapper:

    emotion_abr_to_emotion = None
    emotion_to_emotion_abr = None

    emotion_abr_to_emotion_id = None
    emotion_id_to_emotion_abr = None

    emotion_to_emotion_id = None
    emotion_id_to_emotion = None

    emotion_to_valence = None

    emotion_eng_to_swe = None
    emotion_swe_to_eng = None

    data = None

    @staticmethod
    def _load_data_if_needed():
        # Load data from file if it hasn't been loaded yet
        if Mapper.data is None:
            data_path = resource_filename('nexa_py_sentimotion_mapper',
                                          'nexa-sentimotion-definitions/sentimotion_definitions.json')
            # data_path = "definitions/sentimotion_definitions.json"

            with open(data_path, 'r') as file:
                Mapper.data = json.load(file)
        Mapper.load_mappings(Mapper.data)

    @staticmethod
    def load_mappings(data):

        Mapper.emotion_to_emotion_abr = data["emotion_to_emotion_abr"]
        Mapper.emotion_abr_to_emotion = dict(zip(Mapper.emotion_to_emotion_abr.values(),
                                                 Mapper.emotion_to_emotion_abr.keys()))

        Mapper.emotion_to_emotion_id = data["emotion_to_emotion_id"]
        Mapper.emotion_id_to_emotion = dict(zip(Mapper.emotion_to_emotion_id.values(),
                                                Mapper.emotion_to_emotion_id.keys()))

        Mapper.emotion_abr_to_emotion_id = {}
        for emotion, abr in Mapper.emotion_to_emotion_abr.items():
            Mapper.emotion_abr_to_emotion_id[abr] = Mapper.emotion_to_emotion_id.get(emotion)

        Mapper.emotion_id_to_emotion_abr = dict(zip(Mapper.emotion_abr_to_emotion_id.values(),
                                                    Mapper.emotion_abr_to_emotion_id.keys()))

        Mapper.emotion_to_valence = data["emotion_to_valence"]

        Mapper.emotion_eng_to_swe = data["emotion_eng_to_swe"]
        Mapper.emotion_swe_to_eng = dict(zip(Mapper.emotion_eng_to_swe.values(),
                                             Mapper.emotion_eng_to_swe.keys()))

    @staticmethod
    def translate_values(mapping, input_values):
        # Check if the input is a list or an array
        if isinstance(input_values, (list, tuple, np.ndarray)):
            # If it's a list or tuple, translate each element
            translations = [mapping.get(value) for value in input_values]
            return translations
        else:
            # If it's a single value, translate it directly
            return mapping.get(input_values)

    @staticmethod
    def get_emotion_abr_from_emotion(emotion):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_to_emotion_abr, emotion)

    @staticmethod
    def get_emotion_from_emotion_abr(emotion_abr):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_abr_to_emotion, emotion_abr)

    @staticmethod
    def get_emotion_id_from_emotion(emotion):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_to_emotion_id, emotion)

    @staticmethod
    def get_emotion_from_id(emotion_id):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_id_to_emotion, emotion_id)

    @staticmethod
    def get_emotion_abr_from_emotion_id(emotion_id):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_id_to_emotion_abr, emotion_id)

    @staticmethod
    def get_id_from_emotion_abr(emotion_abr):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_abr_to_emotion_id, emotion_abr)

    @staticmethod
    def get_valence_from_emotion(emotion):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_to_valence, emotion)

    @staticmethod
    def get_swe_translation_from_eng(emotion_eng):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_eng_to_swe, emotion_eng)

    @staticmethod
    def get_eng_translation_from_swe(emotion_swe):
        Mapper._load_data_if_needed()
        return Mapper.translate_values(Mapper.emotion_swe_to_eng, emotion_swe)
