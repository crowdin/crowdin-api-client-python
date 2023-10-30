from crowdin_api.parser import dumps

from crowdin_api.api_resources.abstract.resources import BaseResource


class ApplicationResource(BaseResource):
    """
    Resource for Applications.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Applications

    Link to documentation for enterprise:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Applications
    """

    def get_application_path(self, applicationIdentifier: str, path: str):

        return f"applications/{applicationIdentifier}/api/{path}"

    def get_application_data(self, applicationIdentifier: str, path: str):

        """
        Get the application data
        You can refer to the documentation
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.get
        """
        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, path),
        )

    def update_application_data(self, applicationIdentifier: str, path: str, data: dict):
        """

        Update the application data
        You can refer to the documentation
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.put

        """
        json_data = dumps(data)
        return self.requester.request(
            method="put",
            path=self.get_application_path(applicationIdentifier, path),
            request_data=json_data,
        )

    def add_application_data(self, applicationIdentifier: str, path: str, data: dict):
        """

        Add the application data
        You can refer to the documentation
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.post

        """
        json_data = dumps(data)
        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, path),
            request_data=json_data,
        )

    def delete_application_data(self, applicationIdentifier: str, path: str):
        """

        Delete the application data
        You can refer to the documentation
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.delete

        """
        return self.requester.request(
            method='delete',
            path=self.get_application_path(applicationIdentifier, path)
        )

    def edit_application_data(self, applicationIdentifier: str, path: str, data: dict):
        """

        Edit the application data
        You can refer to the documentation
        https://developer.crowdin.com/api/v2/#operation/api.applications.api.patch

        """
        json_data = dumps(data)
        return self.requester.request(
            method="patch",
            path=self.get_application_path(applicationIdentifier, path),
            request_data=json_data,
        )
