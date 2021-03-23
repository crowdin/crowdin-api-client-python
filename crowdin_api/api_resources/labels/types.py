from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.labels.enums import LabelsPatchPath
from crowdin_api.typing import TypedDict


class LabelsPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: LabelsPatchPath
