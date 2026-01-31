from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import DenormalizePlaceholders, PluralCategoryName
from crowdin_api.sorting import Sorting
from crowdin_api.utils import convert_enum_to_string_if_exists


class StringCorrectionsResource(BaseResource):
    """
    Resource for String Corrections.

    Use API to add or remove strings translations, approvals, and votes.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Corrections
    """

    def get_string_corrections_path(self, project_id: int, correction_id: Optional[int] = None):
        if correction_id is not None:
            return f"projects/{project_id}/corrections/{correction_id}"

        return f"projects/{project_id}/corrections"

    def list_corrections(
        self,
        project_id: int,
        string_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Sorting] = None,
        denormalize_placeholders: Optional[DenormalizePlaceholders] = None,
    ):
        """
        List Corrections

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Corrections/operation/api.projects.corrections.getMany
        """

        params = {
            "stringId": string_id,
            "limit": limit,
            "offset": offset,
            "orderBy": str(order_by) if order_by is not None else None,
            "denormalizePlaceholders": convert_enum_to_string_if_exists(denormalize_placeholders)
        }

        return self.requester.request(
            method="get",
            path=self.get_string_corrections_path(project_id),
            params=params
        )

    def add_correction(
        self,
        project_id: int,
        string_id: int,
        text: str,
        plural_category_name: Optional[PluralCategoryName] = None,
    ):
        """
        Add Correction

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Corrections/operation/api.projects.corrections.post
        """

        params = {
            "stringId": string_id,
            "text": text,
            "pluralCategoryName": convert_enum_to_string_if_exists(plural_category_name),
        }

        return self.requester.request(
            method="post",
            path=self.get_string_corrections_path(project_id),
            request_data=params
        )

    def delete_corrections(
        self,
        project_id: int,
        string_id: int
    ):
        """
        Delete Corrections

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Corrections/operation/api.projects.corrections.deleteMany
        """

        params = {
            "stringId": string_id,
        }

        return self.requester.request(
            method="delete",
            path=self.get_string_corrections_path(project_id),
            params=params
        )

    def get_correction(
        self,
        project_id: int,
        correction_id: int,
        denormalize_placeholders: Optional[DenormalizePlaceholders] = None,
    ):
        """
        Get Correction

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Corrections/operation/api.projects.corrections.get
        """

        return self.requester.request(
            method="get",
            path=self.get_string_corrections_path(project_id, correction_id),
            params={
                "denormalizePlaceholders": convert_enum_to_string_if_exists(denormalize_placeholders),
            }
        )

    def restore_correction(
        self,
        project_id: int,
        correction_id: int,
    ):
        """
        Restore Correction

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Corrections/operation/api.projects.corrections.put
        """

        return self.requester.request(
            method="put",
            path=self.get_string_corrections_path(project_id, correction_id),
        )

    def delete_correction(
        self,
        project_id: int,
        correction_id: int
    ):
        """
        Delete Correction

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Corrections/operation/api.projects.corrections.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_string_corrections_path(project_id, correction_id)
        )