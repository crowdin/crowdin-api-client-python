from typing import Iterable, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict


class DictionaryPatchPath(TypedDict):
    op: PatchOperation
    path: str


class DictionaryPatchRequest(DictionaryPatchPath, total=False):
    """
    Dictionary JSON Patch operation.

    `op` is "add" or "remove". `path` points to a word, e.g. "/words/0" (word index) or
    "/words/-" (append, with "add"). `value` is required for "add" (a word or a list of words).
    To remove several words in one request, specify the word indexes in reverse order.
    """

    value: Union[str, Iterable[str]]
