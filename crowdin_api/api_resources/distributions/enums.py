from enum import Enum


class DistributionPatchPath(Enum):
    EXPORT_MODE = "/exportMode"  # file-based projects only; `exportMode` is deprecated
    NAME = "/name"
    FILE_IDS = "/fileIds"  # file-based projects only; `fileIds` is deprecated, use `/bundleIds`
    BUNDLE_IDS = "/bundleIds"


class ExportMode(Enum):
    DEFAULT = "default"
    BUNDLE = "bundle"
