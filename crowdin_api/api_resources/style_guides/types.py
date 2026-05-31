from typing import Any, Iterable, Optional

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.style_guides.enums import StyleGuidePatchPath
from crowdin_api.typing import TypedDict


class AddStyleGuideRequest(TypedDict):
    name: str
    storageId: int
    aiInstructions: Optional[str]
    languageIds: Optional[Iterable[str]]
    projectIds: Optional[Iterable[int]]
    isShared: Optional[bool]


class StyleGuidePatchRequest(TypedDict):
    op: PatchOperation
    path: StyleGuidePatchPath
    value: Any
