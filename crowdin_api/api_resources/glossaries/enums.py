from enum import Enum


class GlossaryPatchPath(Enum):
    NAME = "/name"


class TermPatchPath(Enum):
    TEXT = "/text"
    DESCRIPTION = "/description"
    PART_OF_SPEECH = "/partOfSpeech"


class TermPartOfSpeech(Enum):
    ADJECTIVE = "adjective"
    ADPOSITION = "adposition"
    ADVERB = "adverb"
    AUXILIARY = "auxiliary"
    COORDINATING_CONJUNCTION = "coordinating conjunction"
    DETERMINER = "determiner"
    INTERJECTION = "interjection"
    NOUN = "noun"
    NUMERAL = "numeral"
    PARTICLE = "particle"
    PRONOUN = "pronoun"
    PROPER_NOUN = "proper noun"
    SUBORDINATING_CONJUNCTION = "subordinating conjunction"
    VERB = "verb"
    OTHER = "other"
