from typing import Any

from crowdin_api.api_resources.bundles.enums import BundlePatchPath
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict


class BundlePatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: BundlePatchPath
