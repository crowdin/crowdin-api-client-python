from enum import Enum


class ListStyleGuidesOrderBy(Enum):
    ID = "id"
    NAME = "name"
    USER_ID = "userId"
    CREATED_AT = "createdAt"


class StyleGuidePatchPath(Enum):
    NAME = "/name"
    AI_INSTRUCTIONS = "/aiInstructions"
    LANGUAGE_IDS = "/languageIds"
    PROJECT_IDS = "/projectIds"
    IS_SHARED = "/isShared"
    STORAGE_ID = "/storageId"
