from typing import List, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.languages.enums import LanguageTextDirection
from crowdin_api.api_resources.languages.types import LanguagesPatchRequest


class LanguagesResource(BaseResource):
    """
    Resource for Languages.

    Crowdin supports more than 300 world languages and custom languages created in the system.

    Use API to get the list of all supported languages and retrieve additional details
    (e.g. text direction, internal code) on specific language.

    Link to documentation: https://support.crowdin.com/api/v2/#tag/Languages
    """

    base_path = "languages"

    def list_supported_languages(
        self,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Supported Languages.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.languages.getMany
        """

        return self.requester.request(
            method="get",
            path=self.prepare_path(),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_custom_language(
        self,
        name: str,
        code: str,
        localeCode: str,
        textDirection: LanguageTextDirection,
        pluralCategoryNames: List[str],
        twoLettersCode: Optional[str] = None,
        dialectOf: Optional[str] = None,
    ):
        """
        Add Custom Language.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.languages.post
        """

        return self.requester.request(
            method="post",
            path=self.prepare_path(),
            post_data={
                "name": name,
                "code": code,
                "localeCode": localeCode,
                "textDirection": textDirection,
                "pluralCategoryNames": pluralCategoryNames,
                "twoLettersCode": twoLettersCode,
                "dialectOf": dialectOf,
            },
        )

    def get_language(self, languageId):
        """
        Get Language.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.languages.get
        """

        return self.requester.request(method="get", path=self.prepare_path(languageId))

    def delete_custom_language(self, languageId):
        """
        Delete Custom Language.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.languages.delete
        """

        return self.requester.request(
            method="delete", path=self.prepare_path(languageId)
        )

    def edit_custom_language(self, languageId, data: List[LanguagesPatchRequest]):
        """
        Edit Custom Language.

        Link to documentation: https://support.crowdin.com/api/v2/#operation/api.languages.patch
        """

        return self.requester.request(
            method="patch",
            path=self.prepare_path(languageId),
            post_data=data,
        )
