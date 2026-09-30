from enum import Enum


class GroupPatchPath(Enum):
    NAME = "/name"
    DESCRIPTION = "/description"
    PARENT_ID = "/parentId"
    SAVINGS_REPORT_SETTINGS_TEMPLATE_ID = "/savingsReportSettingsTemplateId"


class ListGroupsOrderBy(Enum):
    ID = "id"
    NAME = "name"
    DESCRIPTION = "description"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
