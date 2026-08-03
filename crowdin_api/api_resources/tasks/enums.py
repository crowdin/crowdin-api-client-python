from enum import Enum


class TaskOperationPatchPath(Enum):
    STATUS = "/status"
    TITLE = "/title"
    DESCRIPTION = "/description"
    DEADLINE = "/deadline"
    SPLIT_FILES = "/splitFiles"
    FILE_IDS = "/fileIds"
    ASSIGNEES = "/assignees"
    DATE_FROM = "/dateFrom"
    DATE_TO = "/dateTo"
    LABEL_IDS = "/labelIds"
    BATCH_ID = "/batchId"
    RESET_SCOPE = "/resetScope"


class VendorTaskOperationPatchPath(Enum):
    title = "/title"
    description = "/description"
    status = "/status"


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
