from crowdin_api.api_resources.abstract.resources import BaseResource


class OrganizationResource(BaseResource):
    """
    Resource for Organization.

    Crowdin Enterprise only.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Organization
    """

    def get_organization_path(self):
        return "organization"

    def get_organization(self):
        """
        Get Organization.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.organization.get
        """
        return self.requester.request(method="get", path=self.get_organization_path())

    def get_organization_auth_settings(self):
        """
        Get Organization Auth Settings.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.organization.auth-settings.get
        """
        return self.requester.request(
            method="get",
            path=f"{self.get_organization_path()}/auth-settings",
        )
