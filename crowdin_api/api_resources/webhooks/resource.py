from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.webhooks.enums import (
    WebhookContentType,
    WebhookEvents,
    WebhookRequestType,
)
from crowdin_api.api_resources.webhooks.types import WebhookPatchRequest


class WebhooksResource(BaseResource):
    """
    Resource for Webhooks.

    Webhooks allow you to collect information about events that happen in your Crowdin projects.
    You can select the request type, content type, and add a custom payload, which allows you to
    create integrations with other systems on your own.

    You can configure webhooks for the following events:
    -project file is fully translated
    -project file is fully reviewed
    -all strings in project are translated
    -all strings in project are reviewed
    -final translation of string is updated (using Replace in suggestions feature)
    -source string is added
    -source string is updated
    -source string is deleted
    -source string is translated
    -translation for source string is updated (using Replace in suggestions feature)
    -one of translations is deleted
    -translation for string is approved
    -approval for previously added translation is removed

    Use API to create, modify, and delete specific webhooks.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Webhooks
    """

    def get_webhooks_path(self, projectId: int, webhookId: Optional[int] = None):
        if webhookId:
            return f"projects/{projectId}/webhooks/{webhookId}"

        return f"projects/{projectId}/webhooks"

    def list_webhooks(
        self,
        projectId: int,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Webhooks.

        Link to documentation:
        https://support.crowdin.com/api/v2/#tag/Webhooks
        """

        return self.requester.request(
            method="get",
            path=self.get_webhooks_path(projectId=projectId),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_webhook(
        self,
        projectId: int,
        name: str,
        url: str,
        events: Iterable[WebhookEvents],
        requestType: WebhookRequestType,
        isActive: Optional[bool] = None,
        batchingEnabled: Optional[bool] = None,
        contentType: Optional[WebhookContentType] = None,
        headers: Optional[Dict] = None,
        payload: Optional[Dict] = None,
    ):
        """
        Add Webhook.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.webhooks.post
        """

        return self.requester.request(
            method="post",
            path=self.get_webhooks_path(projectId=projectId),
            request_data={
                "name": name,
                "url": url,
                "events": events,
                "requestType": requestType,
                "isActive": isActive,
                "batchingEnabled": batchingEnabled,
                "contentType": contentType,
                "headers": headers,
                "payload": payload,
            },
        )

    def get_webhook(self, projectId: int, webhookId: int):
        """
        Get Webhook.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.webhooks.get
        """

        return self.requester.request(
            method="get", path=self.get_webhooks_path(projectId=projectId, webhookId=webhookId)
        )

    def delete_webhook(self, projectId: int, webhookId: int):
        """
        Delete Webhook.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.webhooks.delete
        """

        return self.requester.request(
            method="delete", path=self.get_webhooks_path(projectId=projectId, webhookId=webhookId)
        )

    def edit_webhook(self, projectId: int, webhookId: int, data: Iterable[WebhookPatchRequest]):
        """
        Edit Custom Language.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.webhooks.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_webhooks_path(projectId=projectId, webhookId=webhookId),
            request_data=data,
        )
