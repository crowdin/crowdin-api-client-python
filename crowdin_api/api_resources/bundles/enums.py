from enum import Enum


class BundlePatchPath(Enum):
    NAME = "/name"
    FORMAT = "/format"
    SOURCE_PATTERNS = "/sourcePatterns"
    IGNORE_PATTERNS = "/ignorePatterns"
    EXPORT_PATTERNS = "/exportPattern"
    DESCRIPTION = "/description"  # no longer listed in the API spec, kept for backward compatibility
    IS_MULTILINGUAL = "/isMultilingual"
    INCLUDE_PROJECT_SOURCE_LANGUAGE = "/includeProjectSourceLanguage"
    INCLUDE_IN_CONTEXT_PSEUDO_LANGUAGE = "/includeInContextPseudoLanguage"
    LABEL_IDS = "/labelIds"
    EXCLUDE_LABEL_IDS = "/excludeLabelIds"
    LABEL_MATCH_RULE = "/labelMatchRule"
    EXCLUDE_LABEL_MATCH_RULE = "/excludeLabelMatchRule"


class BundleLabelMatchRule(Enum):
    ALL = "all"
    ANY = "any"
