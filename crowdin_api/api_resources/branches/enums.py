from enum import Enum


class EditBranchPatchPath(Enum):
    NAME = "/name"
    TITLE = "/title"
    PRIORITY = "/priority"


class ListBranchesOrderBy(Enum):
    ID = "id"
    NAME = "name"
    TITLE = "title"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    EXPORT_PATTERN = "exportPattern"
    PRIORITY = "priority"
