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


class TranslationMemorySegmentBatchOperation(Enum):
    ADD = "add"
    REPLACE = "replace"
    REMOVE = "remove"


class TranslationMemorySegmentBatchOperationPath(Enum):
    ADD = "/-"
    ADD_RECORD = "/{segmentId}/records/-"
    REPLACE = "/{segmentId}/records/{recordId}/text"
    REMOVE = "/{segmentId}"
    REMOVE_RECORD = "/{segmentId}/records/{recordId}"


class ListTmsOrderBy(Enum):
    ID = "id"
    NAME = "name"
    USER_ID = "userId"
    CREATED_AT = "createdAt"


class ListTmSegmentsOrderBy(Enum):
    ID = "id"
