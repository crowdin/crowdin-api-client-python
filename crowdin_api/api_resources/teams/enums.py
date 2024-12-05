from enum import Enum


class TeamPatchPath(Enum):
    NAME = "/name"


class TeamRole(Enum):
    TRANSLATOR = "translator"
    PROOFREADER = "proofreader"


class ListTeamsOrderBy(Enum):
    ID = "id"
    NAME = "name"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
