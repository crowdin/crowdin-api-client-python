from enum import Enum


class MemberRole(Enum):
    """
    Roles for project notifications (`POST /projects/{projectId}/notify`).
    """

    OWNER = "owner"
    MANAGER = "manager"


class OrganizationMemberRole(Enum):
    """
    Roles for organization notifications (`POST /notify`, Crowdin Enterprise only).
    """

    OWNER = "owner"
    ADMIN = "admin"
