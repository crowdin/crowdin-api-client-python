from datetime import datetime
from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.tasks.enums import (
    CrowdinGeneralTaskType,
    CrowdinTaskStatus,
    CrowdinTaskType,
    GengoCrowdinTaskExpertise,
    GengoCrowdinTaskPurpose,
    GengoCrowdinTaskTone,
    OhtCrowdinTaskExpertise,
    OhtCrowdinTaskType,
    TaskOperationPatchPath,
    TranslatedCrowdinTaskExpertise,
    TranslatedCrowdinTaskSubjects,
    ConfigTaskOperationPatchPath,
    LanguageServiceTaskType,
    ManualCrowdinTaskType,
    ManualCrowdinVendors,
)
from crowdin_api.api_resources.tasks.resource import TasksResource, EnterpriseTasksResource
from crowdin_api.requester import APIRequester


class TestTasksResource:
    resource_class = TasksResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1}, "projects/1/tasks/settings-templates"),
            (
                {"projectId": 1, "taskSettingsTemplateId": 2},
                "projects/1/tasks/settings-templates/2"
            ),
        ),
    )
    def test_get_task_settings_templates_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_task_settings_templates_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            ({}, {"offset": 0, "limit": 25}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_task_settings_templates(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_task_settings_templates(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_task_settings_templates_path(projectId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_task_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        input_name = "test template"
        input_config_data = {
            "languages": [
                {
                    "languageId": "uk",
                    "userIds": [1]
                }
            ]
        }

        resource = self.get_resource(base_absolut_url)
        assert resource.add_task_settings_template(
            projectId=1, name=input_name, config=input_config_data
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_task_settings_templates_path(projectId=1),
            request_data={"name": input_name, "config": input_config_data},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_task_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_task_settings_template(
            projectId=1, taskSettingsTemplateId=2
        ) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_task_settings_templates_path(
                projectId=1, taskSettingsTemplateId=2
            )
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_task_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_task_settings_template(
            projectId=1, taskSettingsTemplateId=2
        ) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_task_settings_templates_path(
                projectId=1, taskSettingsTemplateId=2
            )
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "value",
                "op": PatchOperation.REPLACE,
                "path": ConfigTaskOperationPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_task_settings_template(
            projectId=1, taskSettingsTemplateId=2, data=data
        ) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_task_settings_templates_path(projectId=1, taskSettingsTemplateId=2),
        )

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1}, "projects/1/tasks"),
            ({"projectId": 1, "taskId": 2}, "projects/1/tasks/2"),
        ),
    )
    def test_get_tasks_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_tasks_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            ({}, {"assigneeId": None, "status": None, "offset": 0, "limit": 25}),
            (
                {"assigneeId": 1},
                {"assigneeId": 1, "status": None, "offset": 0, "limit": 25},
            ),
            (
                {"status": CrowdinTaskStatus.DONE},
                {"assigneeId": None, "status": CrowdinTaskStatus.DONE, "offset": 0, "limit": 25},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_tasks(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_tasks(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_tasks_path(projectId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_task(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_task(projectId=1, request_data={"some_key": "some_value"}) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_tasks_path(projectId=1),
            request_data={"some_key": "some_value"},
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "status": None,
                    "description": None,
                    "splitContent": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "assignees": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": False,
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": False,
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_general_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_general_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "status": None,
                    "description": None,
                    "splitContent": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "assignees": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": False,
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": False,
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_general_by_string_ids_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_general_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "crowdin_language_service",
                    "status": None,
                    "description": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "includePreTranslatedStringsOnly": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "crowdin_language_service",
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_language_service_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_language_service_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "crowdin_language_service",
                    "status": None,
                    "description": None,
                    "includePreTranslatedStringsOnly": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": LanguageServiceTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "crowdin_language_service",
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_language_service_by_string_ids_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_language_service_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                },
                {
                    "vendor": "oht",
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": None,
                    "description": None,
                    "expertise": None,
                    "editService": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "includePreTranslatedStringsOnly": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "expertise": OhtCrowdinTaskExpertise.AD_WORDS_BANNERS,
                    "editService": True,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "vendor": "oht",
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "expertise": OhtCrowdinTaskExpertise.AD_WORDS_BANNERS,
                    "editService": True,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_oht_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_oht_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                },
                {
                    "vendor": "oht",
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": None,
                    "description": None,
                    "editService": None,
                    "expertise": None,
                    "includePreTranslatedStringsOnly": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "expertise": OhtCrowdinTaskExpertise.AD_WORDS_BANNERS,
                    "editService": True,
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "vendor": "oht",
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": OhtCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "expertise": OhtCrowdinTaskExpertise.AD_WORDS_BANNERS,
                    "editService": True,
                    "includePreTranslatedStringsOnly": False,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_oht_by_string_ids_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_oht_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                },
                {
                    "vendor": "gengo",
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": None,
                    "description": None,
                    "expertise": None,
                    "tone": None,
                    "purpose": None,
                    "customerMessage": None,
                    "usePreferred": None,
                    "editService": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": GengoCrowdinTaskExpertise.PRO,
                    "tone": GengoCrowdinTaskTone.FRIENDLY,
                    "purpose": GengoCrowdinTaskPurpose.APP_OR_WEB_LOCALIZATION,
                    "customerMessage": "customer message",
                    "usePreferred": True,
                    "editService": True,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "vendor": "gengo",
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": GengoCrowdinTaskExpertise.PRO,
                    "tone": GengoCrowdinTaskTone.FRIENDLY,
                    "purpose": GengoCrowdinTaskPurpose.APP_OR_WEB_LOCALIZATION,
                    "customerMessage": "customer message",
                    "usePreferred": True,
                    "editService": True,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_gengo_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_gengo_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                },
                {
                    "vendor": "gengo",
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": None,
                    "description": None,
                    "expertise": None,
                    "editService": None,
                    "tone": None,
                    "purpose": None,
                    "customerMessage": None,
                    "usePreferred": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": GengoCrowdinTaskExpertise.PRO,
                    "tone": GengoCrowdinTaskTone.FRIENDLY,
                    "purpose": GengoCrowdinTaskPurpose.APP_OR_WEB_LOCALIZATION,
                    "customerMessage": "customer message",
                    "usePreferred": True,
                    "editService": True,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "vendor": "gengo",
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": GengoCrowdinTaskExpertise.PRO,
                    "tone": GengoCrowdinTaskTone.FRIENDLY,
                    "purpose": GengoCrowdinTaskPurpose.APP_OR_WEB_LOCALIZATION,
                    "customerMessage": "customer message",
                    "usePreferred": True,
                    "editService": True,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_gengo_by_string_ids_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_gengo_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                },
                {
                    "vendor": "translated",
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": None,
                    "description": None,
                    "expertise": None,
                    "subject": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": TranslatedCrowdinTaskExpertise.ECONOMY,
                    "subject": TranslatedCrowdinTaskSubjects.ART,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "vendor": "translated",
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": TranslatedCrowdinTaskExpertise.ECONOMY,
                    "subject": TranslatedCrowdinTaskSubjects.ART,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_translated_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_translated_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                },
                {
                    "vendor": "translated",
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": None,
                    "description": None,
                    "expertise": None,
                    "subject": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": TranslatedCrowdinTaskExpertise.ECONOMY,
                    "subject": TranslatedCrowdinTaskSubjects.ART,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "vendor": "translated",
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "status": CrowdinTaskStatus.IN_PROGRESS,
                    "description": "description",
                    "expertise": TranslatedCrowdinTaskExpertise.ECONOMY,
                    "subject": TranslatedCrowdinTaskSubjects.ART,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_translated_by_string_ids_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_translated_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "status": None,
                    "description": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "assignees": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "labelIds": [1, 2, 3],
                    "excludeLabelIds": [4, 5, 6],
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "labelIds": [1, 2, 3],
                    "excludeLabelIds": [4, 5, 6],
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_manual_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_manual_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "status": None,
                    "description": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "assignees": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": ManualCrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_manual_by_string_ids_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_manual_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "type": CrowdinTaskType.PROOFREAD,
                    "description": None,
                    "assignees": None,
                    "deadline": None,
                },
            ),
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "type": CrowdinTaskType.PROOFREAD,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_pending_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_pending_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "type": LanguageServiceTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "crowdin_language_service",
                    "description": None,
                    "deadline": None,
                },
            ),
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "deadline": datetime(year=1988, month=9, day=26),
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "deadline": datetime(year=1988, month=9, day=26),
                    "type": LanguageServiceTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "crowdin_language_service",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_language_service_pending_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_language_service_pending_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "type": ManualCrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "description": None,
                    "assignees": None,
                    "deadline": None,
                },
            ),
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "deadline": datetime(year=1988, month=9, day=26),
                    "type": ManualCrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": ManualCrowdinVendors.ACCLARO,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_manual_pending_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_manual_pending_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_task_strings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.export_task_strings(projectId=1, taskId=2) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_tasks_path(projectId=1, taskId=2) + "/exports",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_task(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_task(projectId=1, taskId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_tasks_path(projectId=1, taskId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_task(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_task(projectId=1, taskId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_tasks_path(projectId=1, taskId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "value",
                "op": PatchOperation.REPLACE,
                "path": TaskOperationPatchPath.TITLE,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_task(projectId=1, taskId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_tasks_path(projectId=1, taskId=2),
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            ({}, {"status": None, "offset": 0, "limit": 25}),
            (
                {"status": CrowdinTaskStatus.TODO, "isArchived": False},
                {
                    "status": CrowdinTaskStatus.TODO,
                    "isArchived": False,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_user_tasks(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_user_tasks(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path="user/tasks",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task_archived_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_task_archived_status(projectId=1, taskId=2, isArchived=False)
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path="user/tasks/2",
            params={"projectId": 1},
            request_data=[{"op": "replace", "path": "/isArchived", "value": False}],
        )


class TestEnterpriseTasksResource:
    resource_class = EnterpriseTasksResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_task_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        input_name = "test template"
        input_config_data = {
            "languages": [
                {
                    "languageId": "uk",
                    "userIds": [1],
                    "teamIds": [1]
                }
            ]
        }

        resource = self.get_resource(base_absolut_url)
        assert resource.add_task_settings_template(
            projectId=1, name=input_name, config=input_config_data
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_task_settings_templates_path(projectId=1),
            request_data={"name": input_name, "config": input_config_data},
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "workflowStepId": None,
                    "status": None,
                    "description": None,
                    "splitContent": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "assignees": None,
                    "assignedTeams": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "workflowStepId": 1,
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": True,
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "labelIds": [1, 2, 3],
                    "excludeLabelIds": [4, 5, 6],
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "assignedTeams": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "workflowStepId": 1,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": True,
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "labelIds": [1, 2, 3],
                    "excludeLabelIds": [4, 5, 6],
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "assignedTeams": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_general_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_general_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinGeneralTaskType.TRANSLATE,
                    "workflowStepId": None,
                    "status": None,
                    "description": None,
                    "splitContent": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "assignees": None,
                    "assignedTeams": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "workflowStepId": 1,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": True,
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "assignedTeams": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "workflowStepId": 1,
                    "type": None,
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "splitContent": True,
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "assignedTeams": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_general_by_string_ids_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_general_by_string_ids_task(projectId=1, **incoming_data)
            == "response"
        )
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "fileIds": [1, 2, 3],
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "fileIds": [1, 2, 3],
                    "description": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "fileIds": [1, 2, 3],
                    "description": "description",
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "labelIds": [1, 2, 3],
                    "excludeLabelIds": [4, 5, 6],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "fileIds": [1, 2, 3],
                    "description": "description",
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "labelIds": [1, 2, 3],
                    "excludeLabelIds": [4, 5, 6],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_vendor_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "stringIds": [1, 2, 3],
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "stringIds": [1, 2, 3],
                    "description": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "deadline": None,
                    "startedAt": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "stringIds": [1, 2, 3],
                    "description": "description",
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "workflowStepId": 1,
                    "stringIds": [1, 2, 3],
                    "description": "description",
                    "skipAssignedStrings": True,
                    "includePreTranslatedStringsOnly": True,
                    "deadline": datetime(year=1988, month=9, day=26),
                    "startedAt": datetime(year=1966, month=2, day=1),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_vendor_by_string_ids_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_vendor_by_string_ids_task(projectId=1, **incoming_data)
            == "response"
        )
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "type": CrowdinTaskType.PROOFREAD,
                    "description": None,
                    "assignees": None,
                    "assignedTeams": None,
                    "deadline": None,
                },
            ),
            (
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "assignedTeams": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "type": CrowdinTaskType.PROOFREAD,
                    "description": "description",
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "assignedTeams": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                },
            ),
        ),
    )
    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_pending_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_pending_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data=request_data)
