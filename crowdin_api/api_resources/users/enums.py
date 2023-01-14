from enum import Enum


class UserRole(Enum):
    ALL = "all"
    MANAGER = "manager"
    PROOFREADER = "proofreader"
    TRANSLATOR = "translator"
    BLOCKED = "blocked"


class UserPatchPath(Enum):
    FIRST_NAME = "/firstName"
    LAST_NAME = "/lastName"
    TIMEZONE = "/timezone"
    STATUS = "/status"


class ProjectRole(Enum):
    TRANSLATOR = "translator"
    PROOFREADER = "proofreader"
