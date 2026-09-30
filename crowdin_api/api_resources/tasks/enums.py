from enum import Enum


class TaskOperationPatchPath(Enum):
    """
    Patch paths for Crowdin tasks.

    `FILE_IDS`, `DIRECTORY_IDS` and `SPLIT_FILES` are file-based projects only.
    `SPLIT_FILES` is deprecated, use `SPLIT_CONTENT` instead.
    """

    STATUS = "/status"
    TITLE = "/title"
    DESCRIPTION = "/description"
    DEADLINE = "/deadline"
    STARTED_AT = "/startedAt"
    RESOLVED_AT = "/resolvedAt"
    SPLIT_FILES = "/splitFiles"
    SPLIT_CONTENT = "/splitContent"
    FILE_IDS = "/fileIds"
    DIRECTORY_IDS = "/directoryIds"
    BRANCH_IDS = "/branchIds"
    STRING_IDS = "/stringIds"
    ASSIGNEES = "/assignees"
    DATE_FROM = "/dateFrom"
    DATE_TO = "/dateTo"
    TRANSLATIONS_UPDATED_DATE_FROM = "/translationsUpdatedDateFrom"
    TRANSLATIONS_UPDATED_DATE_TO = "/translationsUpdatedDateTo"
    LABEL_IDS = "/labelIds"
    LABEL_MATCH_RULE = "/labelMatchRule"
    EXCLUDE_LABEL_IDS = "/excludeLabelIds"
    EXCLUDE_LABEL_MATCH_RULE = "/excludeLabelMatchRule"
    SKIP_ASSIGNED_STRINGS = "/skipAssignedStrings"
    RESET_SCOPE = "/resetScope"
    GENERATE_COST_ESTIMATE = "/generateCostEstimate"
    GENERATE_TRANSLATION_COST = "/generateTranslationCost"
    REPORT_SETTINGS_TEMPLATE_ID = "/reportSettingsTemplateId"
    BATCH_ID = "/batchId"


class VendorTaskOperationPatchPath(Enum):
    title = "/title"
    description = "/description"
    status = "/status"


class PendingTaskOperationPatchPath(Enum):
    TITLE = "/title"
    DESCRIPTION = "/description"
    ASSIGNEES = "/assignees"
    DEADLINE = "/deadline"


class VendorPendingTaskOperationPatchPath(Enum):
    TITLE = "/title"
    DESCRIPTION = "/description"


class EnterpriseTaskOperationPatchPath(Enum):
    """
    Patch paths for Crowdin Enterprise tasks.

    `FILE_IDS`, `DIRECTORY_IDS` and `SPLIT_FILES` are file-based projects only.
    `SPLIT_FILES` is deprecated, use `SPLIT_CONTENT` instead.
    To edit a single field value use the `/fields/{fieldSlug}` path as a plain string.
    """

    STATUS = "/status"
    TITLE = "/title"
    DESCRIPTION = "/description"
    DEADLINE = "/deadline"
    STARTED_AT = "/startedAt"
    RESOLVED_AT = "/resolvedAt"
    SPLIT_FILES = "/splitFiles"
    SPLIT_CONTENT = "/splitContent"
    FILE_IDS = "/fileIds"
    DIRECTORY_IDS = "/directoryIds"
    BRANCH_IDS = "/branchIds"
    STRING_IDS = "/stringIds"
    ASSIGNEES = "/assignees"
    ASSIGNED_TEAMS = "/assignedTeams"
    DATE_FROM = "/dateFrom"
    DATE_TO = "/dateTo"
    TRANSLATIONS_UPDATED_DATE_FROM = "/translationsUpdatedDateFrom"
    TRANSLATIONS_UPDATED_DATE_TO = "/translationsUpdatedDateTo"
    LABEL_IDS = "/labelIds"
    LABEL_MATCH_RULE = "/labelMatchRule"
    EXCLUDE_LABEL_IDS = "/excludeLabelIds"
    EXCLUDE_LABEL_MATCH_RULE = "/excludeLabelMatchRule"
    SKIP_ASSIGNED_STRINGS = "/skipAssignedStrings"
    SKIP_ASSIGNED_STRINGS_SCOPE = "/skipAssignedStringsScope"
    FIELDS = "/fields"
    RESET_SCOPE = "/resetScope"
    GENERATE_COST_ESTIMATE = "/generateCostEstimate"
    GENERATE_TRANSLATION_COST = "/generateTranslationCost"
    REPORT_SETTINGS_TEMPLATE_ID = "/reportSettingsTemplateId"
    BATCH_ID = "/batchId"


class EnterpriseVendorTaskOperationPatchPath(Enum):
    """
    Patch paths for Crowdin Enterprise vendor tasks.

    `FILE_IDS` is file-based projects only.
    """

    TITLE = "/title"
    DESCRIPTION = "/description"
    FILE_IDS = "/fileIds"
    STRING_IDS = "/stringIds"
    DATE_FROM = "/dateFrom"
    DATE_TO = "/dateTo"
    TRANSLATIONS_UPDATED_DATE_FROM = "/translationsUpdatedDateFrom"
    TRANSLATIONS_UPDATED_DATE_TO = "/translationsUpdatedDateTo"
    DEADLINE = "/deadline"
    STARTED_AT = "/startedAt"
    RESOLVED_AT = "/resolvedAt"
    LABEL_IDS = "/labelIds"
    LABEL_MATCH_RULE = "/labelMatchRule"
    EXCLUDE_LABEL_IDS = "/excludeLabelIds"
    EXCLUDE_LABEL_MATCH_RULE = "/excludeLabelMatchRule"
    GENERATE_COST_ESTIMATE = "/generateCostEstimate"
    GENERATE_TRANSLATION_COST = "/generateTranslationCost"
    REPORT_SETTINGS_TEMPLATE_ID = "/reportSettingsTemplateId"


class EnterpriseInterOrganizationalTaskOperationPatchPath(Enum):
    """
    Patch paths for Crowdin Enterprise inter-organizational tasks.

    `SPLIT_FILES` is file-based projects only and deprecated, use `SPLIT_CONTENT` instead.
    """

    ASSIGNEE = "/assignee"
    ASSIGNED_TEAMS = "/assignedTeams"
    SPLIT_FILES = "/splitFiles"
    SPLIT_CONTENT = "/splitContent"
    STATUS = "/status"
    GENERATE_COST_ESTIMATE = "/generateCostEstimate"
    GENERATE_TRANSLATION_COST = "/generateTranslationCost"
    REPORT_SETTINGS_TEMPLATE_ID = "/reportSettingsTemplateId"


class EnterprisePendingTaskOperationPatchPath(Enum):
    TITLE = "/title"
    DESCRIPTION = "/description"
    ASSIGNEES = "/assignees"
    ASSIGNED_TEAMS = "/assignedTeams"
    DEADLINE = "/deadline"


class TaskCommentPatchPath(Enum):
    TEXT = "/text"
    TIME_SPENT = "/timeSpent"


class TaskLabelMatchRule(Enum):
    ALL = "all"
    ANY = "any"


class TaskSkipAssignedStringsScope(Enum):
    ALL = "all"
    SAME_WORKFLOW_STEP = "sameWorkflowStep"


class ConfigTaskOperationPatchPath(Enum):
    NAME = "/name"
    CONFIG = "/config"


class CrowdinTaskType(Enum):
    TRANSLATE = 0
    PROOFREAD = 1
    TRANSLATE_BY_VENDOR = 2
    PROOFREAD_BY_VENDOR = 3


class CrowdinGeneralTaskType(Enum):
    TRANSLATE = 0
    PROOFREAD = 1


class CrowdinTaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CLOSED = "closed"


class ListTasksOrderBy(Enum):
    ID = "id"
    TYPE = "type"
    TITLE = "title"
    STATUS = "status"
    DESCRIPTION = "description"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    DEADLINE = "deadline"
    STARTED_AT = "startedAt"
    RESOLVED_AT = "resolvedAt"


class ListUserTasksOrderBy(Enum):
    ID = "id"
    TITLE = "title"
    DESCRIPTION = "description"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    DEADLINE = "deadline"
    STARTED_AT = "startedAt"
    RESOLVED_AT = "resolvedAt"
