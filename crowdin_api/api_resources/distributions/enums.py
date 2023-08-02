from enum import Enum


class DistributionPatchPath(Enum):
    EXPORT_MODE = "/exportMode"
    NAME = "/name"
    FILE_IDS = "/fileIds"
    BUNDLE_IDS = "/bundleIds"


class ExportMode(Enum):
    DEFAULT = "default"
    BUNDLE = "bundle"
