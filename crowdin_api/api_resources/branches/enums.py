from enum import Enum


class EditBranchPatchPath(Enum):
    NAME = "/name"
    TITLE = "/title"
    EXPORT_PATTERN = "/exportPattern"  # file-based projects only
    PRIORITY = "/priority"
    IS_PROTECTED = "/isProtected"  # string-based projects only


class ListBranchesOrderBy(Enum):
    ID = "id"
    NAME = "name"
    TITLE = "title"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    EXPORT_PATTERN = "exportPattern"
    PRIORITY = "priority"
