from enum import Enum


class BundlePatchPath(Enum):
    NAME = "/name"
    FORMAT = "/format"
    SOURCE_PATTERNS = "/sourcePatterns"
    IGNORE_PATTERNS = "/ignorePatterns"
    EXPORT_PATTERNS = "/exportPattern"
    DESCRIPTION = "/description"
    LABEL_IDS = "/labelIds"
