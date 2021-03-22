from enum import Enum


class WebhookEvents(Enum):
    FILE_TRANSLATED = "file.translated"
    FILE_APPROVED = "file.approved"
    PROJECT_TRANSLATED = "project.translated"
    PROJECT_APPROVED = "project.approved"
    TRANSLATION_UPDATED = "translation.updated"
    STRING_ADDED = "string.added"
    STRING_UPDATED = "string.updated"
    STRING_DELETED = "string.deleted"
    SUGGESTION_ADDED = "suggestion.added"
    SUGGESTION_UPDATED = "suggestion.updated"
    SUGGESTION_DELETED = "suggestion.deleted"
    SUGGESTION_APPROVED = "suggestion.approved"
    SUGGESTION_DISAPPROVED = "suggestion.disapproved"


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
