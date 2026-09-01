from typing import Any, Iterable, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.translation_memory.enums import (
    TranslationMemoryPatchPath,
    TranslationMemorySegmentBatchOperation,
    TranslationMemorySegmentBatchOperationPath,
    TranslationMemorySegmentRecordOperation,
    TranslationMemorySegmentRecordOperationPath,
)
from crowdin_api.typing import TypedDict


class TranslationMemoryPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: TranslationMemoryPatchPath


class TranslationMemorySegmentRecord(TypedDict):
    languageId: str
    text: str


class TranslationMemorySegment(TypedDict):
    records: Iterable[TranslationMemorySegmentRecord]


class TranslationMemorySegmentRecordOperationAdd(TypedDict):
    op: TranslationMemorySegmentRecordOperation
    path: TranslationMemorySegmentRecordOperationPath
    value: TranslationMemorySegmentRecord


class TranslationMemorySegmentRecordOperationReplace(TypedDict):
    op: TranslationMemorySegmentRecordOperation
    path: TranslationMemorySegmentRecordOperationPath
    value: str


class TranslationMemorySegmentRecordOperationRemove(TypedDict):
    op: TranslationMemorySegmentRecordOperation
    path: TranslationMemorySegmentRecordOperationPath


class TranslationMemorySegmentBatchOperationAdd(TypedDict):
    op: TranslationMemorySegmentBatchOperation
    path: TranslationMemorySegmentBatchOperationPath
    value: Union[TranslationMemorySegment, TranslationMemorySegmentRecord]


class TranslationMemorySegmentBatchOperationReplace(TypedDict):
    op: TranslationMemorySegmentBatchOperation
    path: TranslationMemorySegmentBatchOperationPath
    value: str


class TranslationMemorySegmentBatchOperationRemove(TypedDict):
    op: TranslationMemorySegmentBatchOperation
    path: TranslationMemorySegmentBatchOperationPath
