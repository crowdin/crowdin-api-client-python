
from typing import TypedDict, Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.webhooks.organization.enums import OrganizationWebhookPatchPath


class OrganizationWebhookPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: OrganizationWebhookPatchPath
