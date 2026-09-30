from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.dictionaries.types import DictionaryPatchRequest


class DictionariesResource(BaseResource):
    """
    Resource for Dictionaries.

    Dictionaries allow you to create a storage of words that should be skipped by the spell checker.

    Use API to get the list of organization dictionaries and to edit a specific dictionary.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Dictionaries
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.dictionaries.getMany
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
        data: Iterable[DictionaryPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Dictionary.

        :param data: JSON Patch operations ("add"/"remove") on "/words/{index}" paths,
            e.g. {"op": "add", "path": "/words/-", "value": "word"} or
            {"op": "remove", "path": "/words/0"}. To remove several words in one request,
            specify the word indexes in reverse order.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.dictionaries.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=f"projects/{projectId}/dictionaries/{languageId}",
            request_data=data,
        )
