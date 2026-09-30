from datetime import datetime
from typing import Any, Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.tasks.enums import (
    CrowdinGeneralTaskType,
    CrowdinTaskStatus,
    CrowdinTaskType,
    TaskLabelMatchRule,
    TaskSkipAssignedStringsScope,
)
from crowdin_api.api_resources.tasks.types import (
    CrowdinTaskAssignee,
    EnterpriseTaskAssignedTeams,
    TaskPatchRequest,
    VendorPatchRequest,
    PendingTaskPatchRequest,
    VendorPendingTaskPatchRequest,
    EnterpriseTaskPatchRequest,
    EnterpriseVendorTaskPatchRequest,
    EnterpriseInterOrganizationalTaskPatchRequest,
    EnterprisePendingTaskPatchRequest,
    ConfigPatchRequest,
    EnterpriseTaskSettingsTemplateLanguages,
    TaskSettingsTemplateLanguages,
)
from crowdin_api.sorting import Sorting
from crowdin_api.utils import convert_to_query_list
from crowdin_api.api_resources.tasks.types import TaskCommentPatchRequest


class TasksResource(BaseResource):
    """
    Resource for Tasks.

    Create and assign tasks to get files translated or proofread by specific people. You can set
    the due dates, split words between people, and receive notifications about the changes and
    updates on tasks. Tasks are project-specific, so you’ll have to create them within a project.

    Use API to create, modify, and delete specific tasks.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Tasks
    """
    def get_task_settings_templates_path(
        self, projectId: int, taskSettingsTemplateId: Optional[int] = None
    ):
        if taskSettingsTemplateId is not None:
            return f"projects/{projectId}/tasks/settings-templates/{taskSettingsTemplateId}"

        return f"projects/{projectId}/tasks/settings-templates"

    def list_task_settings_templates(
        self,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Task Settings Templates.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.settings-templates.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.getMany
        """

        projectId = projectId or self.get_project_id()
        params = self.get_page_params(page=page, offset=offset, limit=limit)

        return self._get_entire_data(
            method="get",
            path=self.get_task_settings_templates_path(projectId=projectId),
            params=params,
        )

    def add_task_settings_template(
        self,
        name: str,
        config: TaskSettingsTemplateLanguages,
        projectId: Optional[int] = None,
    ):
        """
        Add Task Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.settings-templates.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_task_settings_templates_path(projectId=projectId),
            request_data={"name": name, "config": config},
        )

    def get_task_settings_template(
        self, taskSettingsTemplateId: int, projectId: Optional[int] = None
    ):
        """
        Get Task Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.settings-templates.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get", path=self.get_task_settings_templates_path(
                projectId=projectId,
                taskSettingsTemplateId=taskSettingsTemplateId
            )
        )

    def delete_task_settings_template(
        self, taskSettingsTemplateId: int, projectId: Optional[int] = None
    ):
        """
        Delete Task Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.settings-templates.delete

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_task_settings_templates_path(
                projectId=projectId,
                taskSettingsTemplateId=taskSettingsTemplateId
            ),
        )

    def edit_task_settings_template(
        self,
        taskSettingsTemplateId: int,
        data: Iterable[ConfigPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Task Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.settings-templates.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_task_settings_templates_path(
                projectId=projectId,
                taskSettingsTemplateId=taskSettingsTemplateId
            ),
            request_data=data,
        )

    def get_tasks_path(self, projectId: int, taskId: Optional[int] = None):
        if taskId is not None:
            return f"projects/{projectId}/tasks/{taskId}"

        return f"projects/{projectId}/tasks"

    def list_tasks(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        assigneeId: Optional[int] = None,
        status: Optional[Union[CrowdinTaskStatus, Iterable[CrowdinTaskStatus]]] = None,
        batchId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Tasks.

        `status` can be a single status or a list of statuses.
        `assigneeId` is Crowdin only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "assigneeId": assigneeId,
            "status": convert_to_query_list(status),
            "batchId": batchId,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_tasks_path(projectId=projectId),
            params=params,
        )

    def add_task(self, request_data: Dict, projectId: Optional[int] = None):
        """
        Add Task.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_tasks_path(projectId=projectId),
            request_data=request_data,
        )

    def add_general_task(
        self,
        title: str,
        languageId: str,
        fileIds: Optional[Iterable[int]],
        type: CrowdinGeneralTaskType,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        splitContent: Optional[bool] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        batchId: Optional[int] = None,
        directoryIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
        labelMatchRule: Optional[TaskLabelMatchRule] = None,
        excludeLabelMatchRule: Optional[TaskLabelMatchRule] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
    ):
        """
        Add Task(Crowdin Task Create Form, Create By Source Ids Form).

        One of `fileIds`, `directoryIds` or `branchIds` is required (pass `fileIds=None` when
        using `directoryIds` or `branchIds`). `fileIds` and `directoryIds` are file-based
        projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "fileIds": fileIds,
                "type": type,
                "status": status,
                "description": description,
                "splitContent": splitContent,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "assignees": assignees,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "batchId": batchId,
                "directoryIds": directoryIds,
                "branchIds": branchIds,
                "labelMatchRule": labelMatchRule,
                "excludeLabelMatchRule": excludeLabelMatchRule,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
            },
        )

    def add_general_by_string_ids_task(
        self,
        title: str,
        languageId: str,
        stringIds: Iterable[int],
        type: CrowdinGeneralTaskType,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        splitContent: Optional[bool] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        batchId: Optional[int] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
    ):
        """
        Add Task(Crowdin Task Create Form, Create By String Ids Form).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "stringIds": stringIds,
                "type": type,
                "status": status,
                "description": description,
                "splitContent": splitContent,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "assignees": assignees,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "batchId": batchId,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
            },
        )

    def add_vendor_task(
        self,
        title: str,
        languageId: str,
        fileIds: Optional[Iterable[int]],
        type: CrowdinTaskType,
        vendor: str,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        deadline: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        directoryIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
        labelMatchRule: Optional[TaskLabelMatchRule] = None,
        excludeLabelMatchRule: Optional[TaskLabelMatchRule] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
    ):
        """
        Add Task(Crowdin Vendor Task Create Form, Create By Source Ids Form).

        One of `fileIds`, `directoryIds` or `branchIds` is required (pass `fileIds=None` when
        using `directoryIds` or `branchIds`). `fileIds` and `directoryIds` are file-based
        projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "fileIds": fileIds,
                "type": type,
                "vendor": vendor,
                "status": status,
                "description": description,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "deadline": deadline,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "directoryIds": directoryIds,
                "branchIds": branchIds,
                "labelMatchRule": labelMatchRule,
                "excludeLabelMatchRule": excludeLabelMatchRule,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
            },
        )

    def add_vendor_by_string_ids_task(
        self,
        title: str,
        languageId: str,
        stringIds: Iterable[int],
        type: CrowdinTaskType,
        vendor: str,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        deadline: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        labelIds: Optional[Iterable[int]] = None,
        labelMatchRule: Optional[TaskLabelMatchRule] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        excludeLabelMatchRule: Optional[TaskLabelMatchRule] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
    ):
        """
        Add Task(Crowdin Vendor Task Create Form, Create By String Ids Form).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "stringIds": stringIds,
                "type": type,
                "vendor": vendor,
                "status": status,
                "description": description,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "deadline": deadline,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "labelIds": labelIds,
                "labelMatchRule": labelMatchRule,
                "excludeLabelIds": excludeLabelIds,
                "excludeLabelMatchRule": excludeLabelMatchRule,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
            },
        )

    def add_pending_task(
        self,
        title: str,
        precedingTaskId: int,
        projectId: Optional[int] = None,
        description: Optional[str] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        deadline: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Pending Task Create Form).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "precedingTaskId": precedingTaskId,
                "type": CrowdinTaskType.PROOFREAD,
                "title": title,
                "description": description,
                "assignees": assignees,
                "deadline": deadline,
            },
        )

    def add_vendor_pending_task(
        self,
        title: str,
        precedingTaskId: int,
        vendor: str,
        projectId: Optional[int] = None,
        description: Optional[str] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        deadline: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Pending Task Create Form).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "precedingTaskId": precedingTaskId,
                "type": CrowdinTaskType.PROOFREAD_BY_VENDOR,
                "vendor": vendor,
                "title": title,
                "description": description,
                "assignees": assignees,
                "deadline": deadline,
            },
        )

    def export_task_strings(self, taskId: int, projectId: Optional[int] = None):
        """
        Export Task Strings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.exports.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"{self.get_tasks_path(projectId=projectId, taskId=taskId)}/exports",
        )

    def get_task(self, taskId: int, projectId: Optional[int] = None):
        """
        Get Task.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get", path=self.get_tasks_path(projectId=projectId, taskId=taskId)
        )

    def delete_task(self, taskId: int, projectId: Optional[int] = None):
        """
        Delete Task.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_tasks_path(projectId=projectId, taskId=taskId),
        )

    def edit_task(
        self,
        taskId: int,
        data: Union[
            Iterable[VendorPatchRequest],
            Iterable[TaskPatchRequest],
            Iterable[PendingTaskPatchRequest],
            Iterable[VendorPendingTaskPatchRequest],
        ],
        projectId: Optional[int] = None,
    ):
        """
        Edit Task.

        The `/splitFiles` patch path is deprecated, use `/splitContent` instead.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_tasks_path(projectId=projectId, taskId=taskId),
            request_data=data,
        )

    def list_user_tasks(
        self,
        orderBy: Optional[Sorting] = None,
        status: Optional[Union[CrowdinTaskStatus, Iterable[CrowdinTaskStatus]]] = None,
        isArchived: Optional[bool] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List User Tasks (tasks of the authorized user).

        `status` can be a single status or a list of statuses.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.user.tasks.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.user.tasks.getMany
        """

        params = {"orderBy": orderBy, "status": convert_to_query_list(status)}

        if isArchived is not None:
            params["isArchived"] = 1 if isArchived else 0

        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(method="get", path="user/tasks", params=params)

    def _get_tasks_filter_params(
        self,
        orderBy: Optional[Sorting] = None,
        status: Optional[Union[CrowdinTaskStatus, Iterable[CrowdinTaskStatus]]] = None,
        type: Optional[Union[CrowdinTaskType, Iterable[CrowdinTaskType]]] = None,
        projectIds: Optional[Iterable[int]] = None,
        assigneeIds: Optional[Iterable[int]] = None,
        creatorIds: Optional[Iterable[int]] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        sourceLanguageIds: Optional[Iterable[str]] = None,
        createdAtFrom: Optional[datetime] = None,
        createdAtTo: Optional[datetime] = None,
        deadlineFrom: Optional[datetime] = None,
        deadlineTo: Optional[datetime] = None,
    ) -> Dict:
        return {
            "orderBy": orderBy,
            "status": convert_to_query_list(status),
            "type": convert_to_query_list(type),
            "projectIds": convert_to_query_list(projectIds),
            "assigneeIds": convert_to_query_list(assigneeIds),
            "creatorIds": convert_to_query_list(creatorIds),
            "targetLanguageIds": convert_to_query_list(targetLanguageIds),
            "sourceLanguageIds": convert_to_query_list(sourceLanguageIds),
            "createdAtFrom": createdAtFrom,
            "createdAtTo": createdAtTo,
            "deadlineFrom": deadlineFrom,
            "deadlineTo": deadlineTo,
        }

    def list_specific_user_tasks(
        self,
        userId: int,
        orderBy: Optional[Sorting] = None,
        status: Optional[Union[CrowdinTaskStatus, Iterable[CrowdinTaskStatus]]] = None,
        type: Optional[Union[CrowdinTaskType, Iterable[CrowdinTaskType]]] = None,
        projectIds: Optional[Iterable[int]] = None,
        assigneeIds: Optional[Iterable[int]] = None,
        creatorIds: Optional[Iterable[int]] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        sourceLanguageIds: Optional[Iterable[str]] = None,
        createdAtFrom: Optional[datetime] = None,
        createdAtTo: Optional[datetime] = None,
        deadlineFrom: Optional[datetime] = None,
        deadlineTo: Optional[datetime] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List User Tasks (all of the specified user's project tasks).

        Crowdin only. `status` and `type` can be a single value or a list of values.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.tasks.getMany
        """

        params = self._get_tasks_filter_params(
            orderBy=orderBy,
            status=status,
            type=type,
            projectIds=projectIds,
            assigneeIds=assigneeIds,
            creatorIds=creatorIds,
            targetLanguageIds=targetLanguageIds,
            sourceLanguageIds=sourceLanguageIds,
            createdAtFrom=createdAtFrom,
            createdAtTo=createdAtTo,
            deadlineFrom=deadlineFrom,
            deadlineTo=deadlineTo,
        )
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(method="get", path=f"users/{userId}/tasks", params=params)

    # Task Comments
    def get_task_comments_path(
        self,
        projectId: int,
        taskId: int,
        taskCommentId: Optional[int] = None,
    ):
        if taskCommentId is not None:
            return f"projects/{projectId}/tasks/{taskId}/comments/{taskCommentId}"

        return f"projects/{projectId}/tasks/{taskId}/comments"

    def list_task_comments(
        self,
        taskId: int,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Task Comments.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.comments.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"orderBy": orderBy}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_task_comments_path(projectId=projectId, taskId=taskId),
            params=params,
        )

    def add_task_comment(
        self,
        text: str,
        taskId: int,
        projectId: Optional[int] = None,
        timeSpent: Optional[int] = None,
    ):
        """
        Add Task Comment.

        `timeSpent` is the time spent on the task, in seconds.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.comments.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_task_comments_path(projectId=projectId, taskId=taskId),
            request_data={"text": text, "timeSpent": timeSpent},
        )

    def get_task_comment(
        self,
        taskCommentId: int,
        taskId: int,
        projectId: Optional[int] = None,
    ):
        """
        Get Task Comment.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.comments.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_task_comments_path(
                projectId=projectId, taskId=taskId, taskCommentId=taskCommentId
            ),
        )

    def delete_task_comment(
        self,
        taskCommentId: int,
        taskId: int,
        projectId: Optional[int] = None,
    ):
        """
        Delete Task Comment.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.comments.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_task_comments_path(
                projectId=projectId, taskId=taskId, taskCommentId=taskCommentId
            ),
        )

    def edit_task_comment(
        self,
        taskCommentId: int,
        data: Iterable[TaskCommentPatchRequest],
        taskId: int,
        projectId: Optional[int] = None,
    ):
        """
        Edit Task Comment.

        Supported patch paths: `/text` and `/timeSpent` (see `TaskCommentPatchPath`).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.tasks.comments.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_task_comments_path(
                projectId=projectId, taskId=taskId, taskCommentId=taskCommentId
            ),
            request_data=data,
        )

    def edit_task_archived_status(
        self, taskId: int, isArchived: bool = True, projectId: Optional[int] = None
    ):
        """
        Edit Task Archived Status.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.user.tasks.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=f"user/tasks/{taskId}",
            params={"projectId": projectId},
            request_data=[{"op": "replace", "path": "/isArchived", "value": isArchived}],
        )


class EnterpriseTasksResource(TasksResource):
    """
    Resource for Tasks.

    Create and assign tasks to get files translated or proofread by specific people. You can set
    the due dates, split words between people, and receive notifications about the changes and
    updates on tasks. Tasks are project-specific, so you’ll have to create them within a project.

    Use API to create, modify, and delete specific tasks.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Tasks
    """

    def add_task_settings_template(
        self,
        name: str,
        config: EnterpriseTaskSettingsTemplateLanguages,
        projectId: Optional[int] = None,
    ):
        """
        Add Task Settings Template.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_task_settings_templates_path(projectId=projectId),
            request_data={"name": name, "config": config},
        )

    def add_general_task(
        self,
        title: str,
        languageId: str,
        fileIds: Optional[Iterable[int]],
        type: Optional[CrowdinGeneralTaskType],
        workflowStepId: Optional[int] = None,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        splitContent: Optional[bool] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        assignedTeams: Optional[Iterable[EnterpriseTaskAssignedTeams]] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        batchId: Optional[int] = None,
        directoryIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
        labelMatchRule: Optional[TaskLabelMatchRule] = None,
        excludeLabelMatchRule: Optional[TaskLabelMatchRule] = None,
        skipAssignedStringsScope: Optional[TaskSkipAssignedStringsScope] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        """
        Add Task(Enterprise Task Create Form, Create By Source Ids Form).

        One of `fileIds`, `directoryIds` or `branchIds` is required (pass `fileIds=None` when
        using `directoryIds` or `branchIds`). `fileIds` and `directoryIds` are file-based
        projects only. One of `type` or `workflowStepId` is required (pass `type=None` when
        using `workflowStepId`). `status` accepts `todo` or `in_progress`.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "fileIds": fileIds,
                "type": type,
                "workflowStepId": workflowStepId,
                "status": status,
                "description": description,
                "splitContent": splitContent,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "assignees": assignees,
                "assignedTeams": assignedTeams,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "batchId": batchId,
                "directoryIds": directoryIds,
                "branchIds": branchIds,
                "labelMatchRule": labelMatchRule,
                "excludeLabelMatchRule": excludeLabelMatchRule,
                "skipAssignedStringsScope": skipAssignedStringsScope,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
                "fields": fields,
            },
        )

    def add_general_by_string_ids_task(
        self,
        title: str,
        languageId: str,
        stringIds: Iterable[int],
        type: Optional[CrowdinGeneralTaskType] = None,
        workflowStepId: Optional[int] = None,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        splitContent: Optional[bool] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        assignedTeams: Optional[Iterable[EnterpriseTaskAssignedTeams]] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        batchId: Optional[int] = None,
        skipAssignedStringsScope: Optional[TaskSkipAssignedStringsScope] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        """
        Add Task(Enterprise Task Create Form, Create By String Ids Form).

        One of `type` or `workflowStepId` is required. `status` accepts `todo` or `in_progress`.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "stringIds": stringIds,
                "type": type,
                "workflowStepId": workflowStepId,
                "status": status,
                "description": description,
                "splitContent": splitContent,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "assignees": assignees,
                "assignedTeams": assignedTeams,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "batchId": batchId,
                "skipAssignedStringsScope": skipAssignedStringsScope,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
                "fields": fields,
            },
        )

    def add_vendor_task(
        self,
        title: str,
        languageId: str,
        workflowStepId: int,
        fileIds: Optional[Iterable[int]],
        projectId: Optional[int] = None,
        description: Optional[str] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        directoryIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
        labelMatchRule: Optional[TaskLabelMatchRule] = None,
        excludeLabelMatchRule: Optional[TaskLabelMatchRule] = None,
        skipAssignedStringsScope: Optional[TaskSkipAssignedStringsScope] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        """
        Add Task(Enterprise Vendor Task Create Form, Create By Source Ids Form).

        One of `fileIds`, `directoryIds` or `branchIds` is required (pass `fileIds=None` when
        using `directoryIds` or `branchIds`). `fileIds` and `directoryIds` are file-based
        projects only.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "fileIds": fileIds,
                "workflowStepId": workflowStepId,
                "description": description,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateTo": dateTo,
                "directoryIds": directoryIds,
                "branchIds": branchIds,
                "labelMatchRule": labelMatchRule,
                "excludeLabelMatchRule": excludeLabelMatchRule,
                "skipAssignedStringsScope": skipAssignedStringsScope,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
                "fields": fields,
            },
        )

    def add_vendor_by_string_ids_task(
        self,
        title: str,
        languageId: str,
        workflowStepId: int,
        stringIds: Iterable[int],
        projectId: Optional[int] = None,
        description: Optional[str] = None,
        skipAssignedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        labelIds: Optional[Iterable[int]] = None,
        labelMatchRule: Optional[TaskLabelMatchRule] = None,
        skipAssignedStringsScope: Optional[TaskSkipAssignedStringsScope] = None,
        translationsUpdatedDateFrom: Optional[datetime] = None,
        translationsUpdatedDateTo: Optional[datetime] = None,
        generateCostEstimate: Optional[bool] = None,
        generateTranslationCost: Optional[bool] = None,
        reportSettingsTemplateId: Optional[int] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        """
        Add Task(Enterprise Vendor Task Create Form, Create By String Ids Form).

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "stringIds": stringIds,
                "workflowStepId": workflowStepId,
                "description": description,
                "skipAssignedStrings": skipAssignedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateTo": dateTo,
                "labelIds": labelIds,
                "labelMatchRule": labelMatchRule,
                "skipAssignedStringsScope": skipAssignedStringsScope,
                "translationsUpdatedDateFrom": translationsUpdatedDateFrom,
                "translationsUpdatedDateTo": translationsUpdatedDateTo,
                "generateCostEstimate": generateCostEstimate,
                "generateTranslationCost": generateTranslationCost,
                "reportSettingsTemplateId": reportSettingsTemplateId,
                "fields": fields,
            },
        )

    def add_pending_task(
        self,
        title: str,
        precedingTaskId: int,
        projectId: Optional[int] = None,
        description: Optional[str] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        assignedTeams: Optional[Iterable[EnterpriseTaskAssignedTeams]] = None,
        deadline: Optional[datetime] = None,
        type: Optional[CrowdinTaskType] = None,
        workflowStepId: Optional[int] = None,
        vendor: Optional[str] = None,
    ):
        """
        Add Task(Enterprise Pending Task Create Form).

        One of `type` or `workflowStepId` can be provided, not both. When neither is given,
        `type` defaults to `CrowdinTaskType.PROOFREAD`. `vendor` is required for
        `CrowdinTaskType.PROOFREAD_BY_VENDOR`.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        if type is None and workflowStepId is None:
            type = CrowdinTaskType.PROOFREAD

        return self.add_task(
            projectId=projectId,
            request_data={
                "precedingTaskId": precedingTaskId,
                "type": type,
                "workflowStepId": workflowStepId,
                "vendor": vendor,
                "title": title,
                "description": description,
                "assignees": assignees,
                "assignedTeams": assignedTeams,
                "deadline": deadline,
            },
        )

    def edit_task(
        self,
        taskId: int,
        data: Union[
            Iterable[EnterpriseTaskPatchRequest],
            Iterable[EnterpriseVendorTaskPatchRequest],
            Iterable[EnterpriseInterOrganizationalTaskPatchRequest],
            Iterable[EnterprisePendingTaskPatchRequest],
        ],
        projectId: Optional[int] = None,
    ):
        """
        Edit Task.

        The `/splitFiles` patch path is deprecated, use `/splitContent` instead.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.tasks.patch
        """

        return super().edit_task(taskId=taskId, data=data, projectId=projectId)

    def list_organization_tasks(
        self,
        orderBy: Optional[Sorting] = None,
        status: Optional[Union[CrowdinTaskStatus, Iterable[CrowdinTaskStatus]]] = None,
        type: Optional[Union[CrowdinTaskType, Iterable[CrowdinTaskType]]] = None,
        projectIds: Optional[Iterable[int]] = None,
        groupIds: Optional[Iterable[int]] = None,
        assigneeIds: Optional[Iterable[int]] = None,
        creatorIds: Optional[Iterable[int]] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        sourceLanguageIds: Optional[Iterable[str]] = None,
        createdAtFrom: Optional[datetime] = None,
        createdAtTo: Optional[datetime] = None,
        deadlineFrom: Optional[datetime] = None,
        deadlineTo: Optional[datetime] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Tasks (organization level).

        `status` and `type` can be a single value or a list of values.
        `projectIds` cannot be used together with `groupIds`.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.tasks.getMany
        """

        params = self._get_tasks_filter_params(
            orderBy=orderBy,
            status=status,
            type=type,
            projectIds=projectIds,
            assigneeIds=assigneeIds,
            creatorIds=creatorIds,
            targetLanguageIds=targetLanguageIds,
            sourceLanguageIds=sourceLanguageIds,
            createdAtFrom=createdAtFrom,
            createdAtTo=createdAtTo,
            deadlineFrom=deadlineFrom,
            deadlineTo=deadlineTo,
        )
        params["groupIds"] = convert_to_query_list(groupIds)
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(method="get", path="tasks", params=params)
