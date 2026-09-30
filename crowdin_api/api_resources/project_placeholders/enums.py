from enum import Enum


class ProjectPlaceholderType(Enum):
    HIGH = "high"
    LOW = "low"


class ProjectPlaceholderPatchPath(Enum):
    INDEX = "/index"
    TYPE = "/type"
    IS_BLOCKING = "/isBlocking"
    FORMATS = "/formats"
