from enum import Enum


class TranslationMemoryPatchPath(Enum):
    NAME = "/name"


class TranslationMemorySegmentRecordOperation(Enum):
    ADD = "add"
    REPLACE = "replace"
    REMOVE = "remove"


class TranslationMemorySegmentRecordOperationPath(Enum):
    ADD = "/records/-"
    REPLACE = "/records/{recordId}/text"
    REMOVE = "/records/{recordId}"
