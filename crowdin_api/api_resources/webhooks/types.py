from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.webhooks.enums import WebhookPatchPath
from crowdin_api.typing import TypedDict


class WebhookPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: WebhookPatchPath
