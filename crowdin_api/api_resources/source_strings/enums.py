from enum import Enum


class ScopeFilter(Enum):
    ALL = "all"
    IDENTIFIER = "identifier"
    TEXT = "text"
    CONTEXT = "context"
    KEY = "key"


class SourceStringsPatchPath(Enum):
    IDENTIFIER = "/identifier"
    TEXT = "/text"
    CONTEXT = "/context"
    IS_HIDDEN = "/isHidden"
    MAXLENGTH = "/maxLength"
    LABEL_IDS = "/labelIds"
    # Crowdin Enterprise only
    FIELDS = "/fields"
    FIELD = "/fields/{fieldSlug}"


class StringBatchOperations(Enum):
    REPLACE = "replace"
    REMOVE = "remove"
    ADD = "add"


class StringBatchOperationsPath(Enum):
    IDENTIFIER = "/{stringId}/identifier"
    TEXT = "/{stringId}/text"
    CONTEXT = "/{stringId}/context"
    IS_HIDDEN = "/{stringId}/isHidden"
    MAX_LENGTH = "/{stringId}/maxLength"
    LABEL_IDS = "/{stringId}/labelIds"
    # Use with the "remove" operation
    STRING = "/{stringId}"
    # Use with the "add" operation
    NEW_STRING = "/-"


class ListStringsOrderBy(Enum):
    ID = "id"
    TEXT = "text"
    IDENTIFIER = "identifier"
    CONTEXT = "context"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    TYPE = "type"


class StringUpdateOption(Enum):
    """
    Defines whether to keep existing translations and approvals for updated strings.
    """

    KEEP_TRANSLATIONS_AND_APPROVALS = "keep_translations_and_approvals"
    KEEP_TRANSLATIONS = "keep_translations"
    CLEAR_TRANSLATIONS_AND_APPROVALS = "clear_translations_and_approvals"


class UploadStringsType(Enum):
    AUTO = "auto"
    ANDROID = "android"
    MACOSX = "macosx"
    ARB = "arb"
    CSV = "csv"
    JSON = "json"
    XLSX = "xlsx"
    XLIFF = "xliff"
    XLIFF_TWO = "xliff_two"
    RESX = "resx"
    GETTEXT = "gettext"
    I18NEXT_JSON = "i18next_json"
    PROPERTIES = "properties"
    PROPERTIES_XML = "properties_xml"
    PROPERTIES_PLAY = "properties_play"
    YAML = "yaml"
    STRING_CATALOG = "string_catalog"
    NESTJS_I18N = "nestjs_i18n"
    STRINGSDICT = "stringsdict"
