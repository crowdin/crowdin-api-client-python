from enum import Enum


class TeamPatchPath(Enum):
    NAME = "/name"


class TeamRole(Enum):
    TRANSLATOR = "translator"
    PROOFREADER = "proofreader"
