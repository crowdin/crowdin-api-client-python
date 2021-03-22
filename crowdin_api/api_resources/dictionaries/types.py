from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict


class DictionaryPatchPath(TypedDict):
    op: PatchOperation
    path: str
