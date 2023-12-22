from enum import Enum


class UserPermission(Enum):
    OWNER = "owner"
    MANAGERS = "managers"
    ALL = "all"
    GUESTS = "guests"
    RESTRICTED = "restricted"


class ProjectPermission(Enum):
    OWN = "own"
    RESTRICTED = "restricted"
