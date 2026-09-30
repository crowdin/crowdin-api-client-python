from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.system_placeholders.enums import SystemPlaceholderPatchPath
from crowdin_api.typing import TypedDict


class SystemPlaceholderPatchRequest(TypedDict):
    """
    `op` accepts `replace` or `test` only.
    """

    op: PatchOperation
    path: SystemPlaceholderPatchPath
    value: bool
