from enum import Enum


class PreTranslationApplyMethod(Enum):
    TM = "tm"
    MT = "mt"


class ExportProjectTranslationFormat(Enum):
    XLIFF = "xliff"
    ANDROID = "android"
    MACOSX = "macosx"


class VoteMark(Enum):
    UP = "up"
    DOWN = "down"
