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
