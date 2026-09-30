from enum import Enum


class HasManagerAccess(Enum):
    TRUE = 1
    FALSE = 0


class ProjectType(Enum):
    FILE_BASED = 0
    STRING_BASED = 1


class ProjectVisibility(Enum):
    PRIVATE = "private"
    OPEN = "open"


class ProjectLanguageAccessPolicy(Enum):
    OPEN = "open"
    MODERATE = "moderate"


class ProjectPatchPath(Enum):
    """
    JSON Patch paths for Edit Project.

    Crowdin only: `/visibility`, `/languageAccessPolicy`, `/exportApprovedOnly`, `/useGlobalTm`,
    `/tmPreTranslate`, `/mtPreTranslate`, `/aiPreTranslate`.

    Crowdin Enterprise only: `/groupId`, `/taskReviewerIds`, `/exportWithMinApprovalsCount`,
    `/exportStringsThatPassedWorkflow`, `/qaApprovalsCount`, `/fields`, `/fields/{fieldSlug}`, `/tm`,
    `/alignmentActionAiPromptId`, `/templateId`, `/steps`, `/vendorId`, `/mtEngineId`.

    File-based projects only: `/skipUntranslatedFiles`, `/saveMetaInfoInSource`, `/tmContextType`.

    Deprecated: `/glossaryAccess` (use `/glossaryAccessOption` instead) and
    `/preTranslationAiPromptId`.
    """

    NAME = "/name"
    TARGET_LANGUAGE_IDS = "/targetLanguageIds"
    CNAME = "/cname"
    VISIBILITY = "/visibility"
    LANGUAGE_ACCESS_POLICY = "/languageAccessPolicy"
    DESCRIPTION = "/description"
    TRANSLATE_DUPLICATES = "/translateDuplicates"
    IS_MT_ALLOWED = "/isMtAllowed"
    AUTO_SUBSTITUTION = "/autoSubstitution"
    SKIP_UNTRANSLATED_STRINGS = "/skipUntranslatedStrings"
    SKIP_UNTRANSLATED_FILES = "/skipUntranslatedFiles"
    EXPORT_APPROVED_ONLY = "/exportApprovedOnly"
    AUTO_TRANSLATE_DIALECTS = "/autoTranslateDialects"
    PUBLIC_DOWNLOADS = "/publicDownloads"
    USE_GLOBAL_TM = "/useGlobalTm"
    NORMALIZE_PLACEHOLDER = "/normalizePlaceholder"
    SAVE_META_INFO_IN_SOURCE = "/saveMetaInfoInSource"
    IN_CONTEXT = "/inContext"
    IN_CONTEXT_PSEUDO_LANGUAGE_ID = "/inContextPseudoLanguageId"
    QA_CHECK_IS_ACTIVE = "/qaCheckIsActive"
    QA_CHECK_CATEGORIES = "/qaCheckCategories"
    QA_CHECK_CATEGORY = "/qaCheckCategories/{category}"
    QA_CHECKS_IGNORABLE_CATEGORIES = "/qaChecksIgnorableCategories"
    QA_CHECKS_IGNORABLE_CATEGORY = "/qaChecksIgnorableCategories/{category}"
    LANGUAGE_MAPPING = "/languageMapping"
    LANGUAGE_MAPPING_ID = "/languageMapping/{languageId}"
    LANGUAGE_MAPPING_KEY = "/languageMapping/{languageId}/{mappingKey}"
    DEFAULT_TM_ID = "/defaultTmId"
    DEFAULT_GLOSSARY_ID = "/defaultGlossaryId"
    TASK_BASED_ACCESS_CONTROL = "/taskBasedAccessControl"
    SHOW_TM_SUGGESTIONS_DIALECTS = "/showTmSuggestionsDialects"
    TM_APPROVED_SUGGESTIONS_ONLY = "/tmApprovedSuggestionsOnly"
    GLOSSARY_ACCESS = "/glossaryAccess"  # deprecated, use GLOSSARY_ACCESS_OPTION instead
    GLOSSARY_ACCESS_OPTION = "/glossaryAccessOption"
    HIDDEN_STRINGS_PROOFREADERS_ACCESS = "/hiddenStringsProofreadersAccess"
    IN_CONTEXT_PROCESS_HIDDEN_STRINGS = "/inContextProcessHiddenStrings"
    NOTIFICATION_SETTINGS_TRANSLATOR_NEW_STRINGS = "/notificationSettings/translatorNewStrings"
    NOTIFICATION_SETTINGS_MANAGER_NEW_STRINGS = "/notificationSettings/managerNewStrings"
    NOTIFICATION_SETTINGS_MANAGER_LANGUAGE_COMPLETED = (
        "/notificationSettings/managerLanguageCompleted"
    )
    PSEUDO_LANGUAGE_ID = "/pseudoLanguageId"
    ASSIGNED_STYLE_GUIDES = "/assignedStyleGuides"
    ASSIGNED_GLOSSARIES = "/assignedGlossaries"
    ASSIGNED_TMS = "/assignedTms"
    ASSIGNED_TM = "/assignedTms/{tmId}"
    TM_PENALTIES_KEY = "/tmPenalties/{penaltyKey}"
    TM_CONTEXT_TYPE = "/tmContextType"
    TM_PRE_TRANSLATE = "/tmPreTranslate"
    MT_PRE_TRANSLATE = "/mtPreTranslate"
    AI_PRE_TRANSLATE = "/aiPreTranslate"
    PRE_TRANSLATION_AI_PROMPT_ID = "/preTranslationAiPromptId"  # deprecated
    EDITOR_SUGGESTION_AI_PROMPT_ID = "/editorSuggestionAiPromptId"
    QA_CHECK_ACTION_AI_PROMPT_ID = "/qaCheckActionAiPromptId"
    CONTEXT_REVIEW_AI_PROMPT_ID = "/contextReviewAiPromptId"
    SAVINGS_REPORT_SETTINGS_TEMPLATE_ID = "/savingsReportSettingsTemplateId"
    # Crowdin Enterprise only
    GROUP_ID = "/groupId"
    TASK_REVIEWER_IDS = "/taskReviewerIds"
    EXPORT_WITH_MIN_APPROVALS_COUNT = "/exportWithMinApprovalsCount"
    EXPORT_STRINGS_THAT_PASSED_WORKFLOW = "/exportStringsThatPassedWorkflow"
    QA_APPROVALS_COUNT = "/qaApprovalsCount"
    FIELDS = "/fields"
    FIELD = "/fields/{fieldSlug}"
    TM = "/tm"
    ALIGNMENT_ACTION_AI_PROMPT_ID = "/alignmentActionAiPromptId"
    TEMPLATE_ID = "/templateId"
    STEPS = "/steps"
    VENDOR_ID = "/vendorId"
    MT_ENGINE_ID = "/mtEngineId"


class ProjectTranslateDuplicates(Enum):
    SHOW = 0
    HIDE_REGULAR_DETECTION = 1
    SHOW_AUTO_TRANSLATE = 2
    SHOW_REGULAR_DETECTION = 3
    HIDE_STRICT_DETECTION = 4
    SHOW_STRICT_DETECTION = 5


class EscapeQuotes(Enum):
    """
    Values available:
        0 - Do not escape single quote
        1 - Escape single quote by another single quote
        2 - Escape single quote by a backslash
        3 - Escape single quote by another single quote only in strings containing variables
    """
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3


class EscapeSpecialCharacters(Enum):
    """
    Defines whether any special characters (=, :, ! and #) should be escaped by backslash in
    exported translations.
    You can add escape_special_characters per-file option. *

    Acceptable values are:
        0 - Do not escape special characters
        1 - Escape special characters by a backslash
    """
    ZERO = 0
    ONE = 1


class ProjectFilePatchPath(Enum):
    FORMAT = "/format"
    SETTINGS = "/settings"


class ListProjectsOrderBy(Enum):
    ID = "id"
    NAME = "name"
    IDENTIFIER = "identifier"
    DESCRIPTION = "description"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    LAST_ACTIVITY = "lastActivity"


class ProjectTagsDetection(Enum):
    AUTO = 0
    COUNT_TAGS = 1
    SKIP_TAGS = 2


class ProjectGlossaryAccessOption(Enum):
    READ_ONLY = "readOnly"
    FULL_ACCESS = "fullAccess"
    MANAGE_DRAFTS = "manageDrafts"


class ProjectTmContextType(Enum):
    """
    TM perfect match searching mode (file-based projects only).
    """

    SEGMENT_CONTEXT = "segmentContext"
    AUTO = "auto"
    PREV_AND_NEXT_SEGMENT = "prevAndNextSegment"


class TmPreTranslateAutoApproveOption(Enum):
    ALL = "all"
    PERFECT_MATCH_ONLY = "perfectMatchOnly"
    EXCEPT_AUTO_SUBSTITUTED = "exceptAutoSubstituted"
    PERFECT_MATCH_APPROVED_ONLY = "perfectMatchApprovedOnly"
    NONE = "none"


class TmPreTranslateMinimumMatchRatio(Enum):
    PERFECT = "perfect"
    HUNDRED = "100"


class StringsExporterSettingsPatchPath(Enum):
    FORMAT = "/format"
    SETTINGS = "/settings"
