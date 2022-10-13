from enum import Enum


class GlossaryPatchPath(Enum):
    NAME = "/name"


class GlossaryFormat(Enum):
    TBX = "tbx"
    TBX_V3 = "tbx_v3"
    CSV = "csv"
    XLSX = "xlsx"


class GlossaryExportFields(Enum):
    TERM = "term"
    DESCRIPTION = "description"
    PART_OF_SPEECH = "partOfSpeech"
    TYPE = "type"
    STATUS = "status"
    GENDER = "gender"
    NOTE = "note"
    URL = "url"


class TermPatchPath(Enum):
    TEXT = "/text"
    DESCRIPTION = "/description"
    PART_OF_SPEECH = "/partOfSpeech"
    STATUS = "/status"
    TYPE = "/type"
    GENDER = "/gender"
    URL = "/url"
    NOTE = "/note"


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


class TermStatus(Enum):
    PREFERRED = "preferred"
    ADMITTED = "admitted"
    NOT_RECOMMEND = "not recommended"
    OBSOLETE = "obsolete"


class TermType(Enum):
    FULL_FORM = "full form"
    ACRONYM = "acronym"
    ABBREVIATION = "abbreviation"
    SHORT_FORM = "short form"
    PHRASE = "phrase"
    VARIANT = "variant"


class TermGender(Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTER = "neuter"
    OTHER = "other"
