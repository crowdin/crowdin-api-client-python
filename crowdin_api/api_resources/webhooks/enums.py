from enum import Enum


class WebhookEvents(Enum):
    FILE_ADDED = "file.added"
    FILE_UPDATED = "file.updated"
    FILE_REVERTED = "file.reverted"
    FILE_DELETED = "file.deleted"
    FILE_TRANSLATED = "file.translated"
    FILE_APPROVED = "file.approved"
    FILE_QA_FINISHED = "file.qa.finished"
    PROJECT_TRANSLATED = "project.translated"
    PROJECT_APPROVED = "project.approved"
    PROJECT_QA_FINISHED = "project.qa.finished"
    PROJECT_BUILT = "project.built"
    PRE_TRANSLATION_COMPLETED = "preTranslation.completed"
    TRANSLATION_UPDATED = "translation.updated"
    STRING_ADDED = "string.added"
    STRING_UPDATED = "string.updated"
    STRING_DELETED = "string.deleted"
    STRING_COMMENT_CREATED = "stringComment.created"
    STRING_COMMENT_UPDATED = "stringComment.updated"
    STRING_COMMENT_DELETED = "stringComment.deleted"
    STRING_COMMENT_RESTORED = "stringComment.restored"
    SUGGESTION_ADDED = "suggestion.added"
    SUGGESTION_UPDATED = "suggestion.updated"
    SUGGESTION_DELETED = "suggestion.deleted"
    SUGGESTION_APPROVED = "suggestion.approved"
    SUGGESTION_DISAPPROVED = "suggestion.disapproved"
    TASK_ADDED = "task.added"
    TASK_STATUS_CHANGED = "task.statusChanged"
    TASK_UPDATED = "task.updated"
    TASK_DELETED = "task.deleted"


class WebhookRequestType(Enum):
    POST = "POST"
    GET = "GET"


class WebhookContentType(Enum):
    MULTIPART_FORM_DATA = "multipart/form-data"
    APPLICATION_JSON = "application/json"
    APPLICATION_X_WWW_FORM_URLENCODED = "application/x-www-form-urlencoded"


class WebhookPatchPath(Enum):
    NAME = "/name"
    URL = "/url"
    IS_ACTIVE = "/isActive"
    BATCHING_ENABLED = "/batchingEnabled"
    CONTENT_TYPE = "/contentType"
    EVENTS = "/events"
    HEADERS = "/headers"
    REQUEST_TYPE = "/requestType"
    PAYLOAD = "/payload"
