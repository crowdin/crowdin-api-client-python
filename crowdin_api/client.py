import copy
from typing import Optional, Type, Union

from crowdin_api import api_resources
from crowdin_api.requester import APIRequester


class CrowdinClient:
    API_REQUESTER_CLASS: Type[APIRequester] = APIRequester

    TIMEOUT: int = 60
    RETRY_DELAY: Union[int, float] = 0.1  # 100ms
    MAX_RETRIES: Union[int, float] = 5
    HTTP_PROTOCOL: str = "https"
    BASE_URL: str = "api.crowdin.com/api/v2/"

    HEADERS = {}

    ORGANIZATION: Optional[str] = None
    TOKEN = None
    USER_AGENT = "crowdin-api-client-python"
    PAGE_SIZE = 25

    def __init__(self):
        self._api_requestor = None

    @property
    def url(self) -> str:
        if self.ORGANIZATION is None:
            return "{0}://{1}".format(self.HTTP_PROTOCOL, self.BASE_URL)

        return "{0}://{1}.{2}".format(
            self.HTTP_PROTOCOL, self.ORGANIZATION, self.BASE_URL
        )

    def get_default_headers(self) -> dict:
        headers = copy.deepcopy(self.HEADERS or {})
        headers.update(
            {
                "Authorization": "Bearer {0}".format(self.TOKEN),
                "User-Agent": self.USER_AGENT,
            }
        )

        return headers

    def get_api_requestor(self) -> APIRequester:
        if self._api_requestor is None:
            self._api_requestor = self.API_REQUESTER_CLASS(
                base_url=self.url,
                timeout=self.TIMEOUT,
                default_headers=self.get_default_headers(),
            )

        return self._api_requestor

    @property
    def languages(self) -> api_resources.LanguagesResource:
        return api_resources.LanguagesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def projects(self) -> api_resources.ProjectsResource:
        return api_resources.ProjectsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def source_files(self) -> api_resources.SourceFilesResource:
        return api_resources.SourceFilesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def storages(self) -> api_resources.StorageResource:
        return api_resources.StorageResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def translation_status(self) -> api_resources.TranslationStatusResource:
        return api_resources.TranslationStatusResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def translations(self) -> api_resources.TranslationsResource:
        return api_resources.TranslationsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )
