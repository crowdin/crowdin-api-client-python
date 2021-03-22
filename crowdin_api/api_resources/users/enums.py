from enum import Enum


class UserRole(Enum):
    ALL = "all"
    MANAGER = "manager"
    PROOFREADER = "proofreader"
    TRANSLATOR = "translator"
    BLOCKED = "blocked"
