from typing import Union, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.notifications.types import (
    ByRoleRequestScehme,
    ByUserIdsRequestScheme,
    ByOrganizationRoleRequestScheme,
)


class NotificationResource(BaseResource):
    """
    Resource for Notifications.

    Available on both Crowdin and Crowdin Enterprise.
    `send_notification_to_organization_members` is Crowdin Enterprise only.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Notifications

    Link to documentation for enterprise:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Notifications
    """

    def send_notification_to_authenticated_user(self, message: str):
        """
        Send Notification to Authenticated User

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.notify.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.notify.post
        """
        return self.requester.request(
            method="post", path="notify", request_data={"message": message}
        )

    def send_notification_to_project_members(
        self,
        request_data: Union[ByUserIdsRequestScheme, ByRoleRequestScehme],
        projectId: Optional[int] = None,
    ):
        """
        Send Notification To Project Members

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.notify.post

        Link to documentation (Enterprise):
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.notify.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/notify",
            request_data=request_data,
        )

    def send_notification_to_organization_members(
        self,
        request_data: Union[ByUserIdsRequestScheme, ByOrganizationRoleRequestScheme],
    ):
        """
        Send Notification To Organization Members

        Crowdin Enterprise only. Notify organization members by `userIds` or by `role`
        (`owner` or `admin`).

        Link to documentation (Enterprise):
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.notify.post
        """
        return self.requester.request(
            method="post", path="notify", request_data=request_data
        )
