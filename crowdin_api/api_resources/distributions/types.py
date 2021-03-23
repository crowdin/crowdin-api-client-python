from typing import Any

from crowdin_api.api_resources.distributions.enums import DistributionPatchPath
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict


class DistributionPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: DistributionPatchPath
