from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.style_guides.types import (
    AddStyleGuideRequest,
    StyleGuidePatchRequest,
)
from crowdin_api.sorting import Sorting


class StyleGuidesResource(BaseResource):
    """
    Resource for Style Guides.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Style-Guides
    """

    def get_style_guides_path(self, style_guide_id: Optional[int] = None):
        if style_guide_id is not None:
            return f"style-guides/{style_guide_id}"
        return "style-guides"

    def list_style_guides(
        self,
        order_by: Optional[Sorting] = None,
        user_id: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Style Guides

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.style-guides.getMany
        """
        params = {
            "orderBy": order_by,
            "userId": user_id,
        }
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self._get_entire_data(
            method="get",
            path=self.get_style_guides_path(),
            params=params,
        )

    def add_style_guide(self, request_data: AddStyleGuideRequest):
        """
        Create Style Guide

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.style-guides.post
        """
        return self.requester.request(
            method="post",
            path=self.get_style_guides_path(),
            request_data=request_data,
        )

    def get_style_guide(self, style_guide_id: int):
        """
        Get Style Guide

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.style-guides.get
        """
        return self.requester.request(
            method="get",
            path=self.get_style_guides_path(style_guide_id),
        )

    def delete_style_guide(self, style_guide_id: int):
        """
        Delete Style Guide

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.style-guides.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_style_guides_path(style_guide_id),
        )

    def edit_style_guide(
        self,
        style_guide_id: int,
        request_data: Iterable[StyleGuidePatchRequest],
    ):
        """
        Edit Style Guide

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.style-guides.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_style_guides_path(style_guide_id),
            request_data=request_data,
        )
