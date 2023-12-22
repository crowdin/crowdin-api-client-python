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
