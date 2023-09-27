from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.translation_memory.enums import (
    TranslationMemoryPatchPath,
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
