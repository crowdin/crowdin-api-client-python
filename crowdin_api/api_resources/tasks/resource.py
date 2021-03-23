from datetime import datetime
from typing import Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.tasks.enums import (
    CrowdinGeneralTaskType,
    CrowdinTaskStatus,
    GengoCrowdinTaskExpertise,
    GengoCrowdinTaskPurpose,
    GengoCrowdinTaskTone,
    GengoCrowdinTaskType,
    OhtCrowdinTaskExpertise,
    OhtCrowdinTaskType,
    TranslatedCrowdinTaskExpertise,
    TranslatedCrowdinTaskSubjects,
    TranslatedCrowdinTaskType,
)
from crowdin_api.api_resources.tasks.types import (
    CrowdinTaskAssignee,
    TaskPatchRequest,
    VendorPatchRequest,
)


class TasksResource(BaseResource):
    """
    Resource for Tasks.

    Create and assign tasks to get files translated or proofread by specific people. You can set
    the due dates, split words between people, and receive notifications about the changes and
    updates on tasks. Tasks are project-specific, so you’ll have to create them within a project.

    Use API to create, modify, and delete specific tasks.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Tasks
    """

    def get_tasks_path(self, projectId: int, taskId: Optional[int] = None):
        if taskId is not None:
            return f"projects/{projectId}/tasks/{taskId}"

        return f"projects/{projectId}/tasks"

    def list_tasks(
        self,
        projectId: int,
        assigneeId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Tasks.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.getMany
        """

        params = {"assigneeId": assigneeId}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_tasks_path(projectId=projectId),
            params=params,
        )

    def add_task(self, projectId: int, request_data: Dict):
        """
        Add Task.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.post
        """

        return self.requester.request(
            method="post",
            path=self.get_tasks_path(projectId=projectId),
            request_data=request_data,
        )

    def add_general_task(
        self,
        projectId: int,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: CrowdinGeneralTaskType,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        splitFiles: Optional[bool] = None,
        skipAssignedStrings: Optional[bool] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        assignees: Optional[Iterable[CrowdinTaskAssignee]] = None,
        deadline: Optional[datetime] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Task Create Form).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.post
        """

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
                "labelIds": labelIds,
                "assignees": assignees,
                "deadline": deadline,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
            },
        )

    def add_vendor_oht_task(
        self,
        projectId: int,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: OhtCrowdinTaskType,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        expertise: Optional[OhtCrowdinTaskExpertise] = None,
        labelIds: Optional[Iterable[int]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Oht Task Create Form).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.post
        """

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
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "vendor": "oht",
            },
        )

    def add_vendor_gengo_task(
        self,
        projectId: int,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: GengoCrowdinTaskType,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        expertise: Optional[GengoCrowdinTaskExpertise] = None,
        tone: Optional[GengoCrowdinTaskTone] = None,
        purpose: Optional[GengoCrowdinTaskPurpose] = None,
        customerMessage: Optional[str] = None,
        usePreferred: Optional[bool] = None,
        editService: Optional[bool] = None,
        labelIds: Optional[Iterable[int]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Gengo Task Create Form).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.post
        """

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
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "vendor": "gengo",
            },
        )

    def add_vendor_translated_task(
        self,
        projectId: int,
        title: str,
        languageId: str,
        fileIds: Iterable[int],
        type: TranslatedCrowdinTaskType,
        status: Optional[CrowdinTaskStatus] = None,
        description: Optional[str] = None,
        expertise: Optional[TranslatedCrowdinTaskExpertise] = None,
        subject: Optional[TranslatedCrowdinTaskSubjects] = None,
        labelIds: Optional[Iterable[int]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Add Task(Crowdin Vendor Translated Task Create Form).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.post
        """
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
                "dateFrom": dateFrom,
                "dateTo": dateTo,
                "vender": "translated",
            },
        )

    def export_task_strings(self, projectId: int, taskId: int):
        """
        Export Task Strings.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.exports.post
        """

        return self.requester.request(
            method="post", path=f"{self.get_tasks_path(projectId=projectId, taskId=taskId)}/exports"
        )

    def get_task(self, projectId: int, taskId: int):
        """
        Get Task.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.get
        """

        return self.requester.request(
            method="get", path=self.get_tasks_path(projectId=projectId, taskId=taskId)
        )

    def delete_task(self, projectId: int, taskId: int):
        """
        Delete Task.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.delete
        """

        return self.requester.request(
            method="delete", path=self.get_tasks_path(projectId=projectId, taskId=taskId)
        )

    def edit_task(
        self,
        projectId: int,
        taskId: int,
        data: Union[Iterable[VendorPatchRequest], Iterable[TaskPatchRequest]],
    ):
        """
        Edit Task.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.patch
        """

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
        https://support.crowdin.com/api/v2/#operation/api.projects.tasks.getMany
        """

        params = {"status": status}

        if isArchived is not None:
            params["isArchived"] = 1 if isArchived else 0

        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(method="get", path="user/tasks", params=params)

    def edit_task_archived_status(self, taskId: int, projectId: int, isArchived: bool = True):
        """
        Edit Task Archived Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.user.tasks.patch
        """

        return self.requester.request(
            method="patch",
            path=f"user/tasks/{taskId}",
            params={"projectId": projectId},
            request_data=[{"op": "replace", "path": "/isArchived", "value": isArchived}],
        )
