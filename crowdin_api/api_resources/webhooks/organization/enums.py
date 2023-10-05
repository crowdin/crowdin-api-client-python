
from enum import Enum


class OrganizationWebhookEvent(Enum):
    PROJECT_CREATED = "project.created"
    PROJECT_DELETED = "project.deleted"


class EnterpriseOrgWebhookEvent(Enum):
    GROUP_CREATED = "group.created"
    GROUP_DELETED = "group.deleted"
    PROJECT_CREATED = "project.created"
    PROJECT_DELETED = "project.deleted"


class OrganizationWebhookPatchPath(Enum):
    NAME = "/name"
    URL = "/url"
    IS_ACTIVE = "/isActive"
    BATCHING_ENABLED = "/batchingEnabled"
    CONTENT_TYPE = "/contentType"
    EVENTS = "/events"
    HEADERS = "/headers"
    REQUEST_TYPE = "/requestType"
    PAYLOAD = "/payload"
