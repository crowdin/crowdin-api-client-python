from enum import Enum


class UserPermissions(Enum):
    OWNER = "owner"
    MANAGERS = "managers"
    ALL = "all"
    GUESTS = "guests"
    RESTRICTED = "restricted"


class ProjectPermissions(Enum):
    OWN = "own"
    RESTRICTED = "restricted"


class ListApplicationConsentsOrderBy(Enum):
    ID = "id"
    CREATED_AT = "createdAt"


class ApplicationConsentStatus(Enum):
    GRANTED = "granted"
    DENIED = "denied"


class ApplicationConsentPatchPath(Enum):
    STATUS = "/status"
    SCOPES = "/scopes"
