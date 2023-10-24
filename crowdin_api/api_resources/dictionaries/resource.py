from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.dictionaries.types import DictionaryPatchPath


class DictionariesResource(BaseResource):
    """
    Resource for Dictionaries.

    Dictionaries allow you to create a storage of words that should be skipped by the spell checker.

    Use API to get the list of organization dictionaries and to edit a specific dictionary.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Dictionaries
    """

    def list_dictionaries(
        self,
        projectId: Optional[int] = None,
        languageIds: Optional[Iterable[str]] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Dictionaries.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.dictionaries.getMany
        """

        params = self.get_page_params(page=page, offset=offset, limit=limit)
        params["languageIds"] = None if languageIds is None else ",".join(languageIds)
        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/dictionaries",
            params=params,
        )

    def edit_dictionary(
        self,
        languageId: str,
        data: Iterable[DictionaryPatchPath],
        projectId: Optional[int] = None,
    ):
        """
        Edit Dictionary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.dictionaries.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=f"projects/{projectId}/dictionaries/{languageId}",
            request_data=data,
        )
