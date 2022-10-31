from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource


class VendorsResource(BaseResource):
    """
    Resource for Vendors.

    Vendors are the organizations that provide professional translation services.
    To assign a Vendor to a project workflow you should invite an existing Organization
    to be a Vendor for you.

    Use API to get the list of the Vendors you already invited to your organization.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Vendors
    """

    def list_vendors(self, offset: Optional[int] = None, limit: Optional[int] = None):
        """
        List Teams.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.teams.getMany
        """

        return self._get_entire_data(
            method="get",
            path="vendors",
            params=self.get_page_params(offset=offset, limit=limit),
        )
