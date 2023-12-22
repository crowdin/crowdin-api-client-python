from typing import Optional, Iterable
from crowdin_api.parser import dumps
from crowdin_api.api_resources.application.types import (
    ApplicationPermissions,
    ApplicationInstallationPatchRequest,
)
from crowdin_api.api_resources.abstract.resources import BaseResource


class ApplicationResource(BaseResource):
    """
    Crowdin Apps are web applications that can be integrated with Crowdin to extend its functionality.

    Use the API to manage the necessary app data.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Applications

    Link to documentation for enterprise:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Applications
    """

    def get_application_path(self, applicationIdentifier: str, path: str):
        return f"applications/{applicationIdentifier}/api/{path}"

    def get_application_installations_path(self, identifier: Optional[str] = None):
        if identifier:
            return f"applications/installations/{identifier}"
        return "applications/installations"

    def list_application_installations(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Application Installations

        Link to documentaion:
        https://developer.crowdin.com/api/v2/#operation/api.applications.installations.getMany
        """
        return self.requester.request(
            method="get",
            path=self.get_application_installations_path(),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def install_application(
        self, url: str, permissions: Optional[ApplicationPermissions] = None
    ):
        """
        Install Application

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.installations.post
        """
        request_data = {"url": url, "permissions": permissions}
        return self.requester.request(
            method="post",
            path=self.get_application_installations_path(),
            request_data=request_data,
        )

    def get_application_installation(self, identifier: str):
        """
        Get Application Installation

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.installations.get
        """
        return self.requester.request(
            method="get",
            path=self.get_application_installations_path(identifier=identifier),
        )

    def delete_application_installation(
        self, identifier: str, force: Optional[bool] = None
    ):
        """
        Delete Applcation Installation

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.installations.delete
        """
        params = {"force": force}

        return self.requester.request(
            method="delete",
            path=self.get_application_installations_path(identifier=identifier),
            params=params,
        )

    def edit_applicatoin_installation(
        self, identifier: str, data: Iterable[ApplicationInstallationPatchRequest]
    ):
        """
        Edit Application Installation
        """
        return self.requester.request(
            method="patch",
            path=self.get_application_installations_path(identifier=identifier),
            request_data=data,
        )

    def get_application_data(self, applicationIdentifier: str, path: str):
        """
        Get Application Data.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.get

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.applications.api.get
        """

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, path),
        )

    def update_application_data(self, applicationIdentifier: str, path: str, data: dict):
        """
        Update or Restore Application Data.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.put

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.applications.api.put
        """

        json_data = dumps(data)
        return self.requester.request(
            method="put",
            path=self.get_application_path(applicationIdentifier, path),
            request_data=json_data,
        )

    def add_application_data(self, applicationIdentifier: str, path: str, data: dict):
        """
        Add Application Data.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.applications.api.post
        """

        json_data = dumps(data)
        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, path),
            request_data=json_data,
        )

    def delete_application_data(self, applicationIdentifier: str, path: str):
        """
        Delete Application Data.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.delete

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.applications.api.delete
        """

        return self.requester.request(
            method='delete',
            path=self.get_application_path(applicationIdentifier, path)
        )

    def edit_application_data(self, applicationIdentifier: str, path: str, data: dict):
        """
        Edit Application Data.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.patch

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.applications.api.patch
        """

        json_data = dumps(data)
        return self.requester.request(
            method="patch",
            path=self.get_application_path(applicationIdentifier, path),
            request_data=json_data,
        )
