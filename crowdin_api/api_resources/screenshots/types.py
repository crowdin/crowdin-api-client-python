from typing import Any, Optional, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.screenshots.enums import ScreenshotPatchPath, TagPatchPath
from crowdin_api.typing import TypedDict


class ScreenshotPatchRequest(TypedDict):
    value: Any
    op: Union[PatchOperation, str]
    path: ScreenshotPatchPath


class Position(TypedDict):
    x: int
    y: int
    width: int
    height: int


class AddTagRequest(TypedDict):
    stringId: int
    position: Optional[Position]


class TagPatchRequest(TypedDict):
    value: Any
    op: Union[PatchOperation, str]
    path: TagPatchPath
