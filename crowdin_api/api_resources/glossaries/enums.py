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


class GlossaryExportType(Enum):
    CONCEPTS = "concepts"
    TERMS = "terms"


class GlossaryExportStatus(Enum):
    PREFERRED = "PREFERRED"
    ADMITTED = "ADMITTED"
    NOT_RECOMMENDED = "NOT_RECOMMENDED"
    OBSOLETE = "OBSOLETE"
    DRAFT = "DRAFT"


class GlossaryExportPartOfSpeech(Enum):
    NOUN = "NOUN"
    VERB = "VERB"
    ADJECTIVE = "ADJ"
    PRONOUN = "PRON"
    PROPER_NOUN = "PROPN"
    DETERMINER = "DET"
    ADVERB = "ADV"
    ADPOSITION = "ADP"
    COORDINATING_CONJUNCTION = "CCONJ"
    SUBORDINATING_CONJUNCTION = "SCONJ"
    NUMERAL = "NUM"
    INTERJECTION = "INTJ"
    AUXILIARY = "AUX"
    PARTICLE = "PRT"
    SYMBOL = "SYM"
    OTHER = "X"


class GlossaryExportTermType(Enum):
    FULL_FORM = "FULL_FORM"
    ACRONYM = "ACRONYM"
    ABBREVIATION = "ABBREVIATION"
    SHORT_FORM = "SHORT_FORM"
    PHRASE = "PHRASE"
    VARIANT = "VARIANT"


class GlossaryExportGender(Enum):
    MASCULINE = "MASCULINE"
    FEMININE = "FEMININE"
    NEUTER = "NEUTER"
    COMMON = "COMMON"
    OTHER = "OTHER"


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


class ListConceptsOrderBy(Enum):
    ID = "id"
    SUBJECT = "subject"
    DEFINITION = "definition"
    NOTE = "note"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"


class ListGlossariesCrowdinOrderBy(Enum):
    ID = "id"
    NAME = "name"
    USER_ID = "userId"
    CREATED_AT = "createdAt"


class ListGlossariesEnterpriseOrderBy(Enum):
    ID = "id"
    NAME = "name"
    GROUP_ID = "groupId"
    USER_ID = "userId"
    CREATED_AT = "createdAt"


class ListTermsOrderBy(Enum):
    ID = "id"
    TEXT = "text"
    DESCRIPTION = "description"
    PART_OF_SPEECH = "partOfSpeech"
    STATUS = "status"
    TYPE = "type"
    GENDER = "gender"
    NOTE = "note"
    LEMMA = "lemma"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
