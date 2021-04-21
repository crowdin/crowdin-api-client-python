import copy
from typing import Dict, Optional, Type, Union

from crowdin_api import api_resources
from crowdin_api.requester import APIRequester


class CrowdinClient:
    API_REQUESTER_CLASS: Type[APIRequester] = APIRequester

    TIMEOUT: int = 60
    RETRY_DELAY: Union[int, float] = 0.1  # 100ms
    MAX_RETRIES: int = 5
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

        return "{0}://{1}.{2}".format(self.HTTP_PROTOCOL, self.ORGANIZATION, self.BASE_URL)

    def get_default_headers(self) -> Dict:
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
    def dictionaries(self) -> api_resources.DictionariesResource:
        return api_resources.DictionariesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def distributions(self) -> api_resources.DistributionsResource:
        return api_resources.DistributionsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def glossaries(self) -> api_resources.GlossariesResource:
        return api_resources.GlossariesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def labels(self) -> api_resources.LabelsResource:
        return api_resources.LabelsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

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
    def reports(self) -> api_resources.ReportsResource:
        return api_resources.ReportsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def screenshots(self) -> api_resources.ScreenshotsResource:
        return api_resources.ScreenshotsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def source_files(self) -> api_resources.SourceFilesResource:
        return api_resources.SourceFilesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def source_strings(self) -> api_resources.SourceStringsResource:
        return api_resources.SourceStringsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def storages(self) -> api_resources.StoragesResource:
        return api_resources.StoragesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def string_comments(self) -> api_resources.StringCommentsResource:
        return api_resources.StringCommentsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def string_translations(self) -> api_resources.StringTranslationsResource:
        return api_resources.StringTranslationsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def tasks(self) -> api_resources.TasksResource:
        return api_resources.TasksResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def translation_memory(self) -> api_resources.TranslationMemoryResource:
        return api_resources.TranslationMemoryResource(
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

    @property
    def users(self) -> api_resources.UsersResource:
        return api_resources.UsersResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def webhooks(self) -> api_resources.WebhooksResource:
        return api_resources.WebhooksResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )
