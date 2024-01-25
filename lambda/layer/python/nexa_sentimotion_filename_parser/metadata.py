import warnings

from nexa_py_sentimotion_mapper.sentimotion_mapper import Mapper
from nexa_sentimotion_filename_parser.utils import name2list, get_digits_only

from nexa_sentimotion_filename_parser.constants import *


class Metadata(object):

    DEFAULT_INTENSITY_LEVEL = None
    DEFAULT_VERSION = None
    DEFAULT_SITUATION = None

    # can be vocalization (v) or prosody (p)
    DEFAULT_MODE = None

    DEFAULT_PROPORTIONS = None
    DEFAULT_EMOTION_ABR = None
    DEFAULT_MIX = 0
    # set it to some number not in the list
    DEFAULT_EMOTION_ID = 100

    DEFAULT_ERROR = 0

    def __init__(self,
                 filename):
        self.filename = filename
        self.name_list = name2list(filename)

        # e.g. A220
        self.video_id = self.name_list[0]

        self.mix = self.DEFAULT_MIX
        self.emotion_1_abr = self.DEFAULT_EMOTION_ABR
        self.emotion_1_id = self.DEFAULT_EMOTION_ID

        self.emotion_2_abr = self.DEFAULT_EMOTION_ABR
        self.emotion_2_id = self.DEFAULT_EMOTION_ID

        self.proportions = self.DEFAULT_PROPORTIONS
        self.mode = self.DEFAULT_MODE
        self.intensity_level = self.DEFAULT_INTENSITY_LEVEL
        self.version = self.DEFAULT_VERSION
        self.situation = self.DEFAULT_SITUATION

        self.error = self.DEFAULT_ERROR

        self.set_all_metadata(self.name_list)

    def set_mixed_emotions(self, name_list):
        """
        e.g. ang_disg_5050 or ang_disg_50_70
        """
        assert Mapper.get_id_from_emotion_abr(name_list[0]) is not None
        assert Mapper.get_id_from_emotion_abr(name_list[1]) is not None
        assert name_list[2].isdigit() or name_list[2].isdigit() and name_list[3].isdigit()

        self.emotion_1_abr = name_list[0]
        self.emotion_2_abr = name_list[1]
        if len(name_list) == 3:
            self.proportions = int(name_list[2])
        elif len(name_list) == 4:
            self.proportions = int("".join([name_list[2], name_list[3]]))
        else:
            raise ValueError("No interpretable format for emotion mix for filename {}".format(self.filename))

    def set_emotion(self, name_list):
        if len(name_list) == 1:
            if Mapper.get_id_from_emotion_abr(name_list[0]) is not None:
                self.emotion_1_abr = name_list[0]
        elif len(name_list) == 2:
            if name_list in long_emotion_names.values():
                self.emotion_1_abr = "_".join(name_list)
        else:
            raise ValueError("No interpretable format for filename {}".format(self.filename))

    def set_emotion_ids(self):
        self.emotion_1_id = Mapper.get_id_from_emotion_abr(self.emotion_1_abr)
        if self.mix == 1:
            self.emotion_2_id = Mapper.get_id_from_emotion_abr(self.emotion_2_abr)

    def set_all_metadata(self, name_list):

        new_name_list = []

        for item in name_list:
            if video_id_pattern.match(item):
                self.video_id = item
            elif version_pattern.match(item):
                self.version = get_digits_only(item)
            elif item == error:
                self.error = True
            elif situation_pattern.match(item):
                self.situation = get_digits_only(item)
            elif item == mix:
                self.mix = 1
            elif item in modes.values():
                self.mode = item
            elif item in intensity_levels.values():
                self.intensity_level = int(item)
            else:
                new_name_list.append(item)

        if self.mix:
            self.set_mixed_emotions(new_name_list)
        else:
            self.set_emotion(new_name_list)

        self.set_emotion_ids()
