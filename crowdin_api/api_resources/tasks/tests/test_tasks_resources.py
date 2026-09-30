from datetime import datetime
from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.tasks.enums import (
    CrowdinGeneralTaskType,
    CrowdinTaskStatus,
    CrowdinTaskType,
    ListTasksOrderBy,
    ListUserTasksOrderBy,
    TaskOperationPatchPath,
    ConfigTaskOperationPatchPath,
    PendingTaskOperationPatchPath,
    VendorPendingTaskOperationPatchPath,
    EnterpriseTaskOperationPatchPath,
    EnterpriseVendorTaskOperationPatchPath,
    EnterpriseInterOrganizationalTaskOperationPatchPath,
    EnterprisePendingTaskOperationPatchPath,
    TaskCommentPatchPath,
    TaskLabelMatchRule,
    TaskSkipAssignedStringsScope,
)
from crowdin_api.api_resources.tasks.resource import TasksResource, EnterpriseTasksResource
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


COST_FIELDS_NEW = {
    "translationsUpdatedDateFrom": None,
    "translationsUpdatedDateTo": None,
    "generateCostEstimate": None,
    "generateTranslationCost": None,
    "reportSettingsTemplateId": None,
}
C_GENERAL_NEW = {
    "directoryIds": None,
    "branchIds": None,
    "labelMatchRule": None,
    "excludeLabelMatchRule": None,
    **COST_FIELDS_NEW,
}
C_GENERAL_STRING_NEW = {**COST_FIELDS_NEW}
C_VENDOR_NEW = {**C_GENERAL_NEW}
C_VENDOR_STRING_NEW = {
    "labelIds": None,
    "labelMatchRule": None,
    "excludeLabelIds": None,
    "excludeLabelMatchRule": None,
    **COST_FIELDS_NEW,
}
E_GENERAL_NEW = {**C_GENERAL_NEW, "skipAssignedStringsScope": None, "fields": None}
E_GENERAL_STRING_NEW = {**C_GENERAL_STRING_NEW, "skipAssignedStringsScope": None, "fields": None}
E_VENDOR_NEW = {**E_GENERAL_NEW}
E_VENDOR_STRING_NEW = {
    "labelIds": None,
    "labelMatchRule": None,
    "skipAssignedStringsScope": None,
    **COST_FIELDS_NEW,
    "fields": None,
}
E_PENDING_NEW = {"workflowStepId": None, "vendor": None}


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
            (
                {},
                {
                    "orderBy": None,
                    "assigneeId": None,
                    "status": None,
                    "batchId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTasksOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "assigneeId": 1,
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTasksOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "assigneeId": 1,
                    "status": None,
                    "batchId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTasksOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "status": CrowdinTaskStatus.DONE,
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListTasksOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "assigneeId": None,
                    "status": CrowdinTaskStatus.DONE,
                    "batchId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {"batchId": 5},
                {
                    "orderBy": None,
                    "assigneeId": None,
                    "status": None,
                    "batchId": 5,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_tasks(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
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
                    "batchId": None,
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
                    "batchId": 5,
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
                    "batchId": 5,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_general_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_general_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data={**C_GENERAL_NEW, **request_data})

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
                    "batchId": None,
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
                    "batchId": 5,
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
                    "batchId": 5,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_general_by_string_ids_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_general_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data={**C_GENERAL_STRING_NEW, **request_data})

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "gengo",
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "gengo",
                    "status": None,
                    "description": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "deadline": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "oht",
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "oht",
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "labelIds": [4, 5, 6],
                    "excludeLabelIds": [7, 8, 9],
                    "deadline": datetime(year=1988, month=9, day=26),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_task(self, m_add_task, incoming_data, request_data, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data={**C_VENDOR_NEW, **request_data})

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "gengo",
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "vendor": "gengo",
                    "status": None,
                    "description": None,
                    "skipAssignedStrings": None,
                    "includePreTranslatedStringsOnly": None,
                    "deadline": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "oht",
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "deadline": datetime(year=1988, month=9, day=26),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "title": "title",
                    "languageId": "ua",
                    "stringIds": [1, 2, 3],
                    "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "oht",
                    "status": CrowdinTaskStatus.TODO,
                    "description": "description",
                    "skipAssignedStrings": False,
                    "includePreTranslatedStringsOnly": False,
                    "deadline": datetime(year=1988, month=9, day=26),
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_by_string_ids_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_by_string_ids_task(projectId=1, **incoming_data) == "response"
        m_add_task.assert_called_once_with(projectId=1, request_data={**C_VENDOR_STRING_NEW, **request_data})

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
                    "vendor": "crowdin_language_service",
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "crowdin_language_service",
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
                    "vendor": "acclaro",
                    "assignees": [{"id": 1, "wordsCount": 2}],
                    "deadline": datetime(year=1988, month=9, day=26),
                },
                {
                    "title": "title",
                    "precedingTaskId": 1,
                    "description": "description",
                    "deadline": datetime(year=1988, month=9, day=26),
                    "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                    "vendor": "acclaro",
                    "assignees": [{"id": 1, "wordsCount": 2}],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_pending_task(
        self, m_add_task, incoming_data, request_data, base_absolut_url
    ):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vendor_pending_task(projectId=1, **incoming_data) == "response"
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

    @pytest.mark.parametrize(
        "data",
        (
            [
                {
                    "value": "value",
                    "op": PatchOperation.REPLACE,
                    "path": TaskOperationPatchPath.TITLE,
                }
            ],
            [
                {
                    "value": 5,
                    "op": PatchOperation.REPLACE,
                    "path": TaskOperationPatchPath.BATCH_ID,
                }
            ],
            [
                {
                    "value": True,
                    "op": PatchOperation.REPLACE,
                    "path": TaskOperationPatchPath.RESET_SCOPE,
                }
            ],
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task(self, m_request, data, base_absolut_url):
        m_request.return_value = "response"

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
            ({}, {"orderBy": None, "status": None, "offset": 0, "limit": 25}),
            (
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListUserTasksOrderBy.ID,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "status": CrowdinTaskStatus.TODO,
                    "isArchived": False,
                },
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListUserTasksOrderBy.ID,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "status": CrowdinTaskStatus.TODO,
                    "isArchived": False,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_user_tasks(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
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

    # --- Task comments ---
    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1, "taskId": 2}, "projects/1/tasks/2/comments"),
            (
                {"projectId": 1, "taskId": 2, "taskCommentId": 3},
                "projects/1/tasks/2/comments/3",
            ),
        ),
    )
    def test_get_task_comments_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_task_comments_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            ({}, {"orderBy": None, "offset": 0, "limit": 25}),
            ({"orderBy": Sorting([])}, {"orderBy": Sorting([]), "offset": 0, "limit": 25}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_task_comments(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_task_comments(projectId=1, taskId=2, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_task_comments_path(projectId=1, taskId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_task_comment(projectId=1, taskId=2, text="hello") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_task_comments_path(projectId=1, taskId=2),
            request_data={"text": "hello", "timeSpent": None},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_task_comment_with_time_spent(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_task_comment(projectId=1, taskId=2, text="hello", timeSpent=3600)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_task_comments_path(projectId=1, taskId=2),
            request_data={"text": "hello", "timeSpent": 3600},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task_comment_time_spent(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": 120,
                "op": PatchOperation.REPLACE,
                "path": TaskCommentPatchPath.TIME_SPENT,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_task_comment(projectId=1, taskId=2, taskCommentId=3, data=data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_task_comments_path(projectId=1, taskId=2, taskCommentId=3),
            request_data=data,
        )

    COST_FIELDS_VALUES = {
        "translationsUpdatedDateFrom": datetime(year=2024, month=1, day=1),
        "translationsUpdatedDateTo": datetime(year=2024, month=2, day=1),
        "generateCostEstimate": True,
        "generateTranslationCost": False,
        "reportSettingsTemplateId": 7,
    }

    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_general_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"
        new_fields = {
            "directoryIds": [10],
            "branchIds": [11],
            "labelMatchRule": TaskLabelMatchRule.ALL,
            "excludeLabelMatchRule": TaskLabelMatchRule.ANY,
            **self.COST_FIELDS_VALUES,
        }

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_general_task(
                projectId=1,
                title="title",
                languageId="uk",
                fileIds=None,
                type=CrowdinGeneralTaskType.PROOFREAD,
                **new_fields,
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "fileIds": None,
                "type": CrowdinGeneralTaskType.PROOFREAD,
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
                "batchId": None,
                **new_fields,
            },
        )

    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_general_by_string_ids_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_general_by_string_ids_task(
                projectId=1,
                title="title",
                languageId="uk",
                stringIds=[1],
                type=CrowdinGeneralTaskType.TRANSLATE,
                **self.COST_FIELDS_VALUES,
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "stringIds": [1],
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
                "batchId": None,
                **self.COST_FIELDS_VALUES,
            },
        )

    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"
        new_fields = {
            "directoryIds": None,
            "branchIds": [11],
            "labelMatchRule": TaskLabelMatchRule.ANY,
            "excludeLabelMatchRule": TaskLabelMatchRule.ALL,
            **self.COST_FIELDS_VALUES,
        }

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_vendor_task(
                projectId=1,
                title="title",
                languageId="uk",
                fileIds=None,
                type=CrowdinTaskType.TRANSLATE_BY_VENDOR,
                vendor="gengo",
                **new_fields,
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "fileIds": None,
                "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                "vendor": "gengo",
                "status": None,
                "description": None,
                "skipAssignedStrings": None,
                "includePreTranslatedStringsOnly": None,
                "labelIds": None,
                "excludeLabelIds": None,
                "deadline": None,
                "dateFrom": None,
                "dateTo": None,
                **new_fields,
            },
        )

    @mock.patch("crowdin_api.api_resources.tasks.resource.TasksResource.add_task")
    def test_add_vendor_by_string_ids_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"
        new_fields = {
            "labelIds": [1],
            "labelMatchRule": TaskLabelMatchRule.ALL,
            "excludeLabelIds": [2],
            "excludeLabelMatchRule": TaskLabelMatchRule.ANY,
            **self.COST_FIELDS_VALUES,
        }

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_vendor_by_string_ids_task(
                projectId=1,
                title="title",
                languageId="uk",
                stringIds=[1],
                type=CrowdinTaskType.PROOFREAD_BY_VENDOR,
                vendor="oht",
                **new_fields,
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "stringIds": [1],
                "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                "vendor": "oht",
                "status": None,
                "description": None,
                "skipAssignedStrings": None,
                "includePreTranslatedStringsOnly": None,
                "deadline": None,
                "dateFrom": None,
                "dateTo": None,
                **new_fields,
            },
        )

    @pytest.mark.parametrize(
        "path",
        (
            TaskOperationPatchPath.STARTED_AT,
            TaskOperationPatchPath.SPLIT_CONTENT,
            TaskOperationPatchPath.GENERATE_COST_ESTIMATE,
            TaskOperationPatchPath.GENERATE_TRANSLATION_COST,
            TaskOperationPatchPath.REPORT_SETTINGS_TEMPLATE_ID,
            PendingTaskOperationPatchPath.ASSIGNEES,
            VendorPendingTaskOperationPatchPath.DESCRIPTION,
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task_new_paths(self, m_request, path, base_absolut_url):
        m_request.return_value = "response"
        data = [{"value": 1, "op": PatchOperation.REPLACE, "path": path}]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_task(projectId=1, taskId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path="projects/1/tasks/2",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_tasks_multiple_statuses(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_tasks(
                projectId=1, status=[CrowdinTaskStatus.TODO, CrowdinTaskStatus.IN_PROGRESS]
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/tasks",
            params={
                "orderBy": None,
                "assigneeId": None,
                "status": "todo,in_progress",
                "batchId": None,
                "offset": 0,
                "limit": 25,
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_user_tasks_multiple_statuses(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_user_tasks(status=[CrowdinTaskStatus.DONE, CrowdinTaskStatus.CLOSED])
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path="user/tasks",
            params={"orderBy": None, "status": "done,closed", "offset": 0, "limit": 25},
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "orderBy": None,
                    "status": None,
                    "type": None,
                    "projectIds": None,
                    "assigneeIds": None,
                    "creatorIds": None,
                    "targetLanguageIds": None,
                    "sourceLanguageIds": None,
                    "createdAtFrom": None,
                    "createdAtTo": None,
                    "deadlineFrom": None,
                    "deadlineTo": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "orderBy": Sorting([SortingRule(ListTasksOrderBy.ID, SortingOrder.DESC)]),
                    "status": CrowdinTaskStatus.TODO,
                    "type": [CrowdinTaskType.TRANSLATE, CrowdinTaskType.PROOFREAD],
                    "projectIds": [1, 2],
                    "assigneeIds": [3],
                    "creatorIds": [4, 5],
                    "targetLanguageIds": ["uk", "de"],
                    "sourceLanguageIds": ["en"],
                    "createdAtFrom": datetime(year=2024, month=1, day=1),
                    "createdAtTo": datetime(year=2024, month=2, day=1),
                    "deadlineFrom": datetime(year=2024, month=3, day=1),
                    "deadlineTo": datetime(year=2024, month=4, day=1),
                    "limit": 10,
                },
                {
                    "orderBy": Sorting([SortingRule(ListTasksOrderBy.ID, SortingOrder.DESC)]),
                    "status": CrowdinTaskStatus.TODO,
                    "type": "0,1",
                    "projectIds": "1,2",
                    "assigneeIds": "3",
                    "creatorIds": "4,5",
                    "targetLanguageIds": "uk,de",
                    "sourceLanguageIds": "en",
                    "createdAtFrom": datetime(year=2024, month=1, day=1),
                    "createdAtTo": datetime(year=2024, month=2, day=1),
                    "deadlineFrom": datetime(year=2024, month=3, day=1),
                    "deadlineTo": datetime(year=2024, month=4, day=1),
                    "offset": 0,
                    "limit": 10,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_specific_user_tasks(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_specific_user_tasks(userId=12, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="users/12/tasks",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_task_comment(projectId=1, taskId=2, taskCommentId=3) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_task_comments_path(projectId=1, taskId=2, taskCommentId=3),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_task_comment(projectId=1, taskId=2, taskCommentId=3) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_task_comments_path(projectId=1, taskId=2, taskCommentId=3),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task_comment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "new text",
                "op": PatchOperation.REPLACE,
                "path": "/text",
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_task_comment(projectId=1, taskId=2, taskCommentId=3, data=data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_task_comments_path(projectId=1, taskId=2, taskCommentId=3),
            request_data=data,
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
                    "batchId": None,
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
                    "batchId": 5,
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
                    "batchId": 5,
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
        m_add_task.assert_called_once_with(projectId=1, request_data={**E_GENERAL_NEW, **request_data})

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
                    "batchId": None,
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
                    "batchId": 5,
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
                    "batchId": 5,
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
        m_add_task.assert_called_once_with(projectId=1, request_data={**E_GENERAL_STRING_NEW, **request_data})

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
        m_add_task.assert_called_once_with(projectId=1, request_data={**E_VENDOR_NEW, **request_data})

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
        m_add_task.assert_called_once_with(projectId=1, request_data={**E_VENDOR_STRING_NEW, **request_data})

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
        m_add_task.assert_called_once_with(projectId=1, request_data={**E_PENDING_NEW, **request_data})

    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_pending_task_by_workflow_step(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_pending_task(
                projectId=1, title="title", precedingTaskId=1, workflowStepId=5, vendor="oht"
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "precedingTaskId": 1,
                "type": None,
                "workflowStepId": 5,
                "vendor": "oht",
                "title": "title",
                "description": None,
                "assignees": None,
                "assignedTeams": None,
                "deadline": None,
            },
        )

    COST_FIELDS_VALUES = {
        "translationsUpdatedDateFrom": datetime(year=2024, month=1, day=1),
        "translationsUpdatedDateTo": datetime(year=2024, month=2, day=1),
        "generateCostEstimate": True,
        "generateTranslationCost": False,
        "reportSettingsTemplateId": 7,
    }

    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_general_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"
        new_fields = {
            "directoryIds": [10],
            "branchIds": None,
            "labelMatchRule": TaskLabelMatchRule.ALL,
            "excludeLabelMatchRule": TaskLabelMatchRule.ANY,
            "skipAssignedStringsScope": TaskSkipAssignedStringsScope.SAME_WORKFLOW_STEP,
            **self.COST_FIELDS_VALUES,
            "fields": {"some-field": "value"},
        }

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_general_task(
                projectId=1,
                title="title",
                languageId="uk",
                fileIds=None,
                type=None,
                workflowStepId=3,
                status=CrowdinTaskStatus.IN_PROGRESS,
                **new_fields,
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "fileIds": None,
                "type": None,
                "workflowStepId": 3,
                "status": CrowdinTaskStatus.IN_PROGRESS,
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
                "batchId": None,
                **new_fields,
            },
        )

    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_general_by_string_ids_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"
        new_fields = {
            "skipAssignedStringsScope": TaskSkipAssignedStringsScope.ALL,
            **self.COST_FIELDS_VALUES,
            "fields": {"some-field": 1},
        }

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_general_by_string_ids_task(
                projectId=1, title="title", languageId="uk", stringIds=[1], **new_fields
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "stringIds": [1],
                "type": None,
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
                "batchId": None,
                **new_fields,
            },
        )

    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_vendor_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"
        new_fields = {
            "directoryIds": None,
            "branchIds": [2],
            "labelMatchRule": TaskLabelMatchRule.ANY,
            "excludeLabelMatchRule": TaskLabelMatchRule.ALL,
            "skipAssignedStringsScope": TaskSkipAssignedStringsScope.ALL,
            **self.COST_FIELDS_VALUES,
            "fields": {"some-field": True},
        }

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_vendor_task(
                projectId=1,
                title="title",
                languageId="uk",
                workflowStepId=3,
                fileIds=None,
                **new_fields,
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "fileIds": None,
                "workflowStepId": 3,
                "description": None,
                "skipAssignedStrings": None,
                "includePreTranslatedStringsOnly": None,
                "labelIds": None,
                "excludeLabelIds": None,
                "deadline": None,
                "startedAt": None,
                "dateTo": None,
                **new_fields,
            },
        )

    @mock.patch(
        "crowdin_api.api_resources.tasks.resource.EnterpriseTasksResource.add_task"
    )
    def test_add_vendor_by_string_ids_task_new_fields(self, m_add_task, base_absolut_url):
        m_add_task.return_value = "response"
        new_fields = {
            "labelIds": [1],
            "labelMatchRule": TaskLabelMatchRule.ALL,
            "skipAssignedStringsScope": TaskSkipAssignedStringsScope.SAME_WORKFLOW_STEP,
            **self.COST_FIELDS_VALUES,
            "fields": {"some-field": "value"},
        }

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_vendor_by_string_ids_task(
                projectId=1,
                title="title",
                languageId="uk",
                workflowStepId=3,
                stringIds=[1, 2],
                **new_fields,
            )
            == "response"
        )
        m_add_task.assert_called_once_with(
            projectId=1,
            request_data={
                "title": "title",
                "languageId": "uk",
                "stringIds": [1, 2],
                "workflowStepId": 3,
                "description": None,
                "skipAssignedStrings": None,
                "includePreTranslatedStringsOnly": None,
                "deadline": None,
                "startedAt": None,
                "dateTo": None,
                **new_fields,
            },
        )

    @pytest.mark.parametrize(
        "path",
        (
            EnterpriseTaskOperationPatchPath.ASSIGNED_TEAMS,
            EnterpriseTaskOperationPatchPath.SKIP_ASSIGNED_STRINGS_SCOPE,
            EnterpriseTaskOperationPatchPath.FIELDS,
            "/fields/some-field",
            EnterpriseVendorTaskOperationPatchPath.REPORT_SETTINGS_TEMPLATE_ID,
            EnterpriseInterOrganizationalTaskOperationPatchPath.GENERATE_COST_ESTIMATE,
            EnterpriseInterOrganizationalTaskOperationPatchPath.GENERATE_TRANSLATION_COST,
            EnterpriseInterOrganizationalTaskOperationPatchPath.REPORT_SETTINGS_TEMPLATE_ID,
            EnterprisePendingTaskOperationPatchPath.ASSIGNED_TEAMS,
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_task(self, m_request, path, base_absolut_url):
        m_request.return_value = "response"
        data = [{"value": 1, "op": PatchOperation.REPLACE, "path": path}]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_task(projectId=1, taskId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path="projects/1/tasks/2",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "orderBy": None,
                    "status": None,
                    "type": None,
                    "projectIds": None,
                    "groupIds": None,
                    "assigneeIds": None,
                    "creatorIds": None,
                    "targetLanguageIds": None,
                    "sourceLanguageIds": None,
                    "createdAtFrom": None,
                    "createdAtTo": None,
                    "deadlineFrom": None,
                    "deadlineTo": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "orderBy": Sorting([SortingRule(ListTasksOrderBy.ID, SortingOrder.ASC)]),
                    "status": [CrowdinTaskStatus.TODO, CrowdinTaskStatus.DONE],
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "groupIds": [1, 2],
                    "assigneeIds": [3, 4],
                    "creatorIds": [5],
                    "targetLanguageIds": ["uk"],
                    "sourceLanguageIds": ["en", "fr"],
                    "createdAtFrom": datetime(year=2024, month=1, day=1),
                    "createdAtTo": datetime(year=2024, month=2, day=1),
                    "deadlineFrom": datetime(year=2024, month=3, day=1),
                    "deadlineTo": datetime(year=2024, month=4, day=1),
                    "offset": 5,
                },
                {
                    "orderBy": Sorting([SortingRule(ListTasksOrderBy.ID, SortingOrder.ASC)]),
                    "status": "todo,done",
                    "type": CrowdinTaskType.TRANSLATE_BY_VENDOR,
                    "projectIds": None,
                    "groupIds": "1,2",
                    "assigneeIds": "3,4",
                    "creatorIds": "5",
                    "targetLanguageIds": "uk",
                    "sourceLanguageIds": "en,fr",
                    "createdAtFrom": datetime(year=2024, month=1, day=1),
                    "createdAtTo": datetime(year=2024, month=2, day=1),
                    "deadlineFrom": datetime(year=2024, month=3, day=1),
                    "deadlineTo": datetime(year=2024, month=4, day=1),
                    "offset": 5,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_organization_tasks(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_organization_tasks(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="tasks",
            params=request_params,
        )
