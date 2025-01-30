from typing import Optional, Iterable

from crowdin_api.api_resources.abstract.resources import BaseResource
from .enums import LanguageRecognitionProvider


class MachineTranslationEnginesResource(BaseResource):
    """
    Resource for Machine Translation Engines.

    Machine Translation Engines (MTE) are the sources for pre-translations.

    Use API to add, update, and delete specific MTE.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Machine-Translation-Engines
    """

    def get_mts_path(self, mtId: Optional[int] = None):
        if mtId is not None:
            return f"mts/{mtId}"

        return "mts"

    def list_mts(self, limit: Optional[int] = None, offset: Optional[int] = None):
        """
        List MTs.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.mts.getMany
        """

        return self._get_entire_data(
            method="get",
            path=self.get_mts_path(),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def get_mt(self, mtId: int):
        """
        Get MT.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.mts.get
        """

        return self.requester.request(method="get", path=self.get_mts_path(mtId=mtId))

    def translate_via_mt(
        self,
        mtId: int,
        targetLanguageId: str = None,
        languageRecognitionProvider: Optional[LanguageRecognitionProvider] = None,
        sourceLanguageId: Optional[str] = None,
        strings: Optional[Iterable[str]] = None,
    ):
        """
        Create Translate via MT.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.mts.translations.post
        """
        return self.requester.request(
            method="post",
            path=f"{self.get_mts_path(mtId=mtId)}/translations",
            request_data={
                "targetLanguageId": targetLanguageId,
                "languageRecognitionProvider": languageRecognitionProvider,
                "sourceLanguageId": sourceLanguageId,
                "strings": strings,
            },
        )
