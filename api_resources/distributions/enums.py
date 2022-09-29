from enum import Enum


class DistributionPatchPath(Enum):
    EXPORT_MODE = "/exportMode"
    NAME = "/name"
    FILE_IDS = "/fileIds"
    FORMAT = "/format"
    EXPORT_PATTERN = "/exportPattern"
    LABEL_IDS = "/labelIds"


class ExportMode(Enum):
    DEFAULT = "default"
    BUNDLE = "bundle"
