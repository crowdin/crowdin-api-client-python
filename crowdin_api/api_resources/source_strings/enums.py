from enum import Enum


class ScopeFilter(Enum):
    IDENTIFIER = "identifier"
    TEXT = "text"
    CONTEXT = "context"


class SourceStringsPatchPath(Enum):
    TEXT = "/text"
    CONTEXT = "/context"
    IS_HIDDEN = "/isHidden"
    MAXLENGTH = "/maxLength"
    LABEL_IDS = "/labelIds"


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


class ListStringsOrderBy(Enum):
    ID = "id"
    TEXT = "text"
    IDENTIFIER = "identifier"
    CONTEXT = "context"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    TYPE = "type"
