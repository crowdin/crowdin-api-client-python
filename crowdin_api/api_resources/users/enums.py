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


class ListProjectMembersCrowdinOrderBy(Enum):
    ID = "id"
    USERNAME = "username"
    FULL_NAME = "fullName"


class ListProjectMembersEnterpriseOrderBy(Enum):
    ID = "id"
    USERNAME = "username"
    FIRST_NAME = "firstName"
    LAST_NAME = "lastName"


class ListGroupManagersOrderBy(Enum):
    ID = "id"
    USERNAME = "username"
    EMAIL = "email"
    STATUS = "status"
    CREATED_AT = "createdAt"
    LAST_SEEN = "lastSeen"


class ListGroupTeamsOrderBy(Enum):
    ID = "id"
    NAME = "name"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
