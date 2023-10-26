from datetime import datetime
from typing import Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.tasks.enums import (
    CrowdinGeneralTaskType,
    CrowdinTaskStatus,
    LanguageServiceTaskType,
    GengoCrowdinTaskExpertise,
    GengoCrowdinTaskPurpose,
    GengoCrowdinTaskTone,
    GengoCrowdinTaskType,
    OhtCrowdinTaskExpertise,
    OhtCrowdinTaskType,
    TranslatedCrowdinTaskExpertise,
    TranslatedCrowdinTaskSubjects,
    TranslatedCrowdinTaskType,
    ManualCrowdinTaskType,
    ManualCrowdinVendors,
)
from crowdin_api.api_resources.tasks.types import (
    CrowdinTaskAssignee,
    TaskPatchRequest,
    VendorPatchRequest,
    ConfigPatchRequest,
    EnterpriseTaskSettingsTemplateLanguages,
    TaskSettingsTemplateLanguages,
)


class TasksResource(BaseResource):
    """
    Resource for Tasks.

    Create and assign tasks to get files translated or proofread by specific people. You can set
    the due dates, split words between people, and receive notifications about the changes and
    updates on tasks. Tasks are project-specific, so you’ll have to create them within a project.

    Use API to create, modify, and delete specific tasks.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Tasks
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.settings-templates.getMany

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.getMany
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.settings-templates.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.settings-templates.get

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.get
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.settings-templates.delete

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.delete
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.settings-templates.patch

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.patch
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
        assigneeId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Tasks.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"assigneeId": assigneeId, "status": status}
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.post
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
        fileIds: Iterable[int],
        type: CrowdinGeneralTaskType,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        splitFiles: Optional[bool] = None,
        skipAssignedStrings: Optional[bool] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Task Create Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.post
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
                "splitFiles": splitFiles,
                "skipAssignedStrings": skipAssignedStrings,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "assignees": assignees,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
            },
        )

    def add_language_service_task(
        self,
        title: str,
        languageId: str,
        fileIds: Iterable[str],
        type: LanguageServiceTaskType,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        includeUntranslatedStringsOnly: Optional[bool] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Language Service Task Create Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.post
        """

        projectId = projectId or self.get_project_id()

        return self.add_task(
            projectId=projectId,
            request_data={
                "title": title,
                "languageId": languageId,
                "fileIds": fileIds,
                "type": type,
                "vendor": "crowdin_language_service",
                "status": status,
                "description": description,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "includeUntranslatedStringsOnly": includeUntranslatedStringsOnly,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
            }
        )

    def add_vendor_oht_task(
        self,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: OhtCrowdinTaskType,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        expertise: Optional[OhtCrowdinTaskExpertise] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        includeUntranslatedStringsOnly: Optional[bool] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Oht Task Create Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.post
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
                "expertise": expertise,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "includeUntranslatedStringsOnly": includeUntranslatedStringsOnly,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "vendor": "oht",
            },
        )

    def add_vendor_gengo_task(
        self,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: GengoCrowdinTaskType,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        expertise: Optional[GengoCrowdinTaskExpertise] = None,
        tone: Optional[GengoCrowdinTaskTone] = None,
        purpose: Optional[GengoCrowdinTaskPurpose] = None,
        customerMessage: Optional[str] = None,
        usePreferred: Optional[bool] = None,
        editService: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Gengo Task Create Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.post
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
                "expertise": expertise,
                "tone": tone,
                "purpose": purpose,
                "customerMessage": customerMessage,
                "usePreferred": usePreferred,
                "editService": editService,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "vendor": "gengo",
            },
        )

    def add_vendor_translated_task(
        self,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: TranslatedCrowdinTaskType,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        expertise: Optional[TranslatedCrowdinTaskExpertise] = None,
        subject: Optional[TranslatedCrowdinTaskSubjects] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Translated Task Create Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.post
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
                "expertise": expertise,
                "subject": subject,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "vender": "translated",
            },
        )

    def add_vendor_manual_task(
        self,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: ManualCrowdinTaskType,
        vendor: ManualCrowdinVendors,
        projectId: Optional[int] = None,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        skipAssignedStrings: Optional[bool] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        includePreTranslatedStringsOnly: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        deadline: Optional[datetime] = None,
        startedAt: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Manual Task Create Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.post
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
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "includePreTranslatedStringsOnly": includePreTranslatedStringsOnly,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "assignees": assignees,
                "deadline": deadline,
                "startedAt": startedAt,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
            },
        )

    def export_task_strings(self, taskId: int, projectId: Optional[int] = None):
        """
        Export Task Strings.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.exports.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get", path=self.get_tasks_path(projectId=projectId, taskId=taskId)
        )

    def delete_task(self, taskId: int, projectId: Optional[int] = None):
        """
        Delete Task.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_tasks_path(projectId=projectId, taskId=taskId),
        )

    def edit_task(
        self,
        taskId: int,
        data: Union[Iterable[VendorPatchRequest], Iterable[TaskPatchRequest]],
        projectId: Optional[int] = None,
    ):
        """
        Edit Task.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_tasks_path(projectId=projectId, taskId=taskId),
            request_data=data,
        )

    def list_user_tasks(
        self,
        status: Optional[CrowdinTaskStatus] = None,
        isArchived: Optional[bool] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Tasks.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tasks.getMany
        """

        params = {"status": status}

        if isArchived is not None:
            params["isArchived"] = 1 if isArchived else 0

        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(method="get", path="user/tasks", params=params)

    def edit_task_archived_status(
        self, taskId: int, isArchived: bool = True, projectId: Optional[int] = None
    ):
        """
        Edit Task Archived Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.user.tasks.patch
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
    https://developer.crowdin.com/enterprise/api/v2/#tag/Tasks
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
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.tasks.settings-templates.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_task_settings_templates_path(projectId=projectId),
            request_data={"name": name, "config": config},
        )
