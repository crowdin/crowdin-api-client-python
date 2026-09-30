from enum import Enum


class ScreenshotPatchPath(Enum):
    NAME = "/name"
    LABEL_IDS = "/labelIds"


class TagPatchPath(Enum):
    STRING_ID = "/stringId"
    POSITION = "/position"


class ListScreenshotsOrderBy(Enum):
    ID = "id"
    NAME = "name"
    TAGS_COUNT = "tagsCount"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
