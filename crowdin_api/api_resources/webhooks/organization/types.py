
from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.webhooks.organization.enums import OrganizationWebhookPatchPath
from crowdin_api.typing import TypedDict


class OrganizationWebhookPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: OrganizationWebhookPatchPath
