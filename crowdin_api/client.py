import copy
from typing import Dict, Optional, Type, Union

from crowdin_api import api_resources
from crowdin_api.enums import PlatformType
from crowdin_api.exceptions import CrowdinException
from crowdin_api.requester import APIRequester


class CrowdinClient:
    API_REQUESTER_CLASS: Type[APIRequester] = APIRequester

    PROJECT_ID = None
    TIMEOUT = 60
    RETRY_DELAY = 0.1  # 100ms
    MAX_RETRIES = 5
    HTTP_PROTOCOL = "https"
    TOKEN = None
    ORGANIZATION = None
    BASE_URL = "api.crowdin.com/api/v2/"
    HEADERS = {}
    USER_AGENT = "crowdin-api-client-python"
    PAGE_SIZE = 25
    EXTENDED_REQUEST_PARAMS = None

    def __init__(
        self,
        # TODO: replace this with union type expressions
        # once we do not have to support <3.10 anymore
        project_id: Optional[int] = None,
        organization: Optional[str] = None,
        token: Optional[str] = None,
        base_url: Optional[str] = None,
        user_agent: Optional[str] = None,
        page_size: Optional[int] = None,
        timeout: Optional[int] = None,
        retry_delay: Union[int, float, None] = None,
        max_retries: Optional[int] = None,
        http_protocol: Optional[str] = None,
        headers: Optional[dict] = None,
        extended_request_params: Optional[dict] = None
    ):
        self.PROJECT_ID = project_id or self.PROJECT_ID
        self.ORGANIZATION = organization or self.ORGANIZATION
        self.TOKEN = token or self.TOKEN
        self.BASE_URL = base_url or self.BASE_URL
        self.USER_AGENT = user_agent or self.USER_AGENT
        self.PAGE_SIZE = page_size or self.PAGE_SIZE
        self.TIMEOUT = timeout or self.TIMEOUT
        self.RETRY_DELAY = retry_delay or self.RETRY_DELAY
        self.MAX_RETRIES = max_retries or self.MAX_RETRIES
        self.HTTP_PROTOCOL = http_protocol or self.HTTP_PROTOCOL
        self.HEADERS = headers or self.HEADERS
        self.EXTENDED_REQUEST_PARAMS = extended_request_params or self.EXTENDED_REQUEST_PARAMS
        self._api_requestor = None

        if self.ORGANIZATION is None:
            self._platform_type = PlatformType.BASIC
        else:
            self._platform_type = PlatformType.ENTERPRISE

    @property
    def url(self) -> str:
        if not self._is_enterprise_platform:
            return "{0}://{1}".format(self.HTTP_PROTOCOL, self.BASE_URL)

        return "{0}://{1}.{2}".format(self.HTTP_PROTOCOL, self.ORGANIZATION, self.BASE_URL)

    @property
    def _is_enterprise_platform(self) -> bool:
        return self._platform_type == PlatformType.ENTERPRISE

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
                retry_delay=self.RETRY_DELAY,
                max_retries=self.MAX_RETRIES,
                default_headers=self.get_default_headers(),
                extended_params=self.EXTENDED_REQUEST_PARAMS
            )
        return self._api_requestor

    def graphql(self, query: str, variables: Optional[Dict] = None) -> Dict:
        data = {
            "query": query,
            "variables": variables or {}
        }
        return self.get_api_requestor().request(
            method="post",
            path="graphql",
            request_data=data
        )

    @property
    def ai(self) -> Union[api_resources.AIResource, api_resources.EnterpriseAIResource]:
        if self._is_enterprise_platform:
            ai_class = api_resources.EnterpriseAIResource
        else:
            ai_class = api_resources.AIResource

        if self.PROJECT_ID:
            return ai_class(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )
        return ai_class(requester=self.get_api_requestor(), page_size=self.PAGE_SIZE)

    @property
    def applications(self) -> api_resources.ApplicationResource:
        return api_resources.ApplicationResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def bundles(self) -> api_resources.BundlesResource:
        if self.PROJECT_ID:
            return api_resources.BundlesResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.BundlesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def dictionaries(self) -> api_resources.DictionariesResource:
        if self.PROJECT_ID:
            return api_resources.DictionariesResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.DictionariesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def distributions(self) -> api_resources.DistributionsResource:
        if self.PROJECT_ID:
            return api_resources.DistributionsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.DistributionsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def fields(self) -> api_resources.FieldsResource:
        if not self._is_enterprise_platform:
            raise CrowdinException(detail="Not implemented for the base API")

        if self.PROJECT_ID:
            return api_resources.FieldsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.FieldsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def glossaries(self) -> api_resources.GlossariesResource:
        if self.PROJECT_ID:
            return api_resources.GlossariesResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.GlossariesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def groups(self) -> api_resources.GroupsResource:
        if not self._is_enterprise_platform:
            raise CrowdinException(detail="Not implemented for the base API")

        if self.PROJECT_ID:
            return api_resources.GroupsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.GroupsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def labels(self) -> api_resources.LabelsResource:
        if self.PROJECT_ID:
            return api_resources.LabelsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.LabelsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def languages(self) -> api_resources.LanguagesResource:
        if self.PROJECT_ID:
            return api_resources.LanguagesResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.LanguagesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def projects(self) -> api_resources.ProjectsResource:
        if self.PROJECT_ID:
            return api_resources.ProjectsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.ProjectsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def reports(self) -> Union[api_resources.ReportsResource,
                               api_resources.EnterpriseReportsResource]:

        if self._is_enterprise_platform:
            report_class = api_resources.EnterpriseReportsResource
        else:
            report_class = api_resources.ReportsResource

        if self.PROJECT_ID:
            return report_class(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return report_class(
            requester=self.get_api_requestor(),
            page_size=self.PAGE_SIZE,
        )

    @property
    def screenshots(self) -> api_resources.ScreenshotsResource:
        if self.PROJECT_ID:
            return api_resources.ScreenshotsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.ScreenshotsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def security_logs(self) -> api_resources.SecurityLogsResource:
        if self.PROJECT_ID:
            return api_resources.SecurityLogsResource(
                requester=self.get_api_requestor(),
                page_size=self.PAGE_SIZE,
                project_id=self.PROJECT_ID,
            )

        return api_resources.SecurityLogsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE,
        )

    @property
    def source_files(self) -> api_resources.SourceFilesResource:
        if self.PROJECT_ID:
            return api_resources.SourceFilesResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.SourceFilesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def source_strings(self) -> api_resources.SourceStringsResource:
        if self.PROJECT_ID:
            return api_resources.SourceStringsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.SourceStringsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def storages(self) -> api_resources.StoragesResource:
        if self.PROJECT_ID:
            return api_resources.StoragesResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.StoragesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def string_comments(self) -> api_resources.StringCommentsResource:
        if self.PROJECT_ID:
            return api_resources.StringCommentsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.StringCommentsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def string_translations(self) -> api_resources.StringTranslationsResource:
        if self.PROJECT_ID:
            return api_resources.StringTranslationsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.StringTranslationsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def tasks(self) -> Union[api_resources.TasksResource, api_resources.EnterpriseTasksResource]:
        if self._is_enterprise_platform:
            report_class = api_resources.EnterpriseTasksResource
        else:
            report_class = api_resources.TasksResource

        if self.PROJECT_ID:
            return report_class(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return report_class(
            requester=self.get_api_requestor(),
            page_size=self.PAGE_SIZE,
        )

    @property
    def teams(self) -> api_resources.TeamsResource:
        if not self._is_enterprise_platform:
            raise CrowdinException(detail="Not implemented for the base API")

        if self.PROJECT_ID:
            return api_resources.TeamsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.TeamsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def translation_memory(self) -> api_resources.TranslationMemoryResource:
        if self.PROJECT_ID:
            return api_resources.TranslationMemoryResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.TranslationMemoryResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def translation_status(self) -> api_resources.TranslationStatusResource:
        if self.PROJECT_ID:
            return api_resources.TranslationStatusResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.TranslationStatusResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def translations(self) -> api_resources.TranslationsResource:
        if self.PROJECT_ID:
            return api_resources.TranslationsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.TranslationsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def machine_translations(self) -> api_resources.MachineTranslationEnginesResource:
        if self.PROJECT_ID:
            return api_resources.MachineTranslationEnginesResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.MachineTranslationEnginesResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def users(self) -> Union[api_resources.UsersResource, api_resources.EnterpriseUsersResource]:
        if self._is_enterprise_platform:
            user_class = api_resources.EnterpriseUsersResource
        else:
            user_class = api_resources.UsersResource

        if self.PROJECT_ID:
            return user_class(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return user_class(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def vendors(self) -> api_resources.VendorsResource:
        if not self._is_enterprise_platform:
            raise CrowdinException(detail="Not implemented for the base API")

        if self.PROJECT_ID:
            return api_resources.VendorsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.VendorsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def webhooks(self) -> api_resources.WebhooksResource:
        if self.PROJECT_ID:
            return api_resources.WebhooksResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.WebhooksResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )

    @property
    def workflows(self) -> api_resources.WorkflowsResource:
        if not self._is_enterprise_platform:
            raise CrowdinException(detail="Not implemented for the base API")

        if self.PROJECT_ID:
            return api_resources.WorkflowsResource(
                requester=self.get_api_requestor(),
                project_id=self.PROJECT_ID,
                page_size=self.PAGE_SIZE,
            )

        return api_resources.WorkflowsResource(
            requester=self.get_api_requestor(), page_size=self.PAGE_SIZE
        )
