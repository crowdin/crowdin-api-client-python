from enum import Enum


class PreTranslationApplyMethod(Enum):
    TM = "tm"
    MT = "mt"


class VoteMark(Enum):
    UP = "up"
    DOWN = "down"
