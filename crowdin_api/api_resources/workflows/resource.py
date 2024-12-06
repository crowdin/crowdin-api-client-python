from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.sorting import Sorting


class WorkflowsResource(BaseResource):
    """
    Resource for Workflows.

    Workflows are the sequences of steps that content in your project should go through
    (e.g. pre-translation, translation, proofreading). You can use a default template or create
    the one that works best for you and assign it to the needed projects.

    Use API to get the list of workflow templates available in your organization and to check
    the details of a specific template.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Workflows
    """

    def get_workflow_steps_path(self, projectId: int, stepId: Optional[int] = None):
        if stepId:
            return f"projects/{projectId}/workflow-steps/{stepId}"

        return f"projects/{projectId}/workflow-steps"

    def get_workflow_templates_path(self, templateId: Optional[int] = None):
        if templateId:
            return f"workflow-templates/{templateId}"

        return "workflow-templates"

    def list_workflow_steps(self, projectId: Optional[int] = None):
        """
        List Workflow Steps.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.workflow-steps.getMany
        """
        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_workflow_steps_path(projectId=projectId),
        )

    def get_workflow_step(self, stepId: int, projectId: Optional[int] = None):
        """
        Get Workflow Step.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.workflow-steps.get
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_workflow_steps_path(projectId=projectId, stepId=stepId),
        )

    def list_workflow_templates(
        self,
        groupId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ):
        """
        List Workflow Templates.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.workflow-templates.getMany
        """
        params = {"groupId": groupId}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_workflow_templates_path(),
            params=params,
        )

    def get_workflow_template(self, templateId: int):
        """
        Get Workflow Template.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.workflow-templates.get
        """
        return self.requester.request(
            method="get",
            path=self.get_workflow_templates_path(templateId=templateId),
        )

    def get_workflow_step_strings_path(self, projectId: int, stepId: int):
        return f"projects/{projectId}/workflow-steps/{stepId}/strings"

    def list_workflow_step_strings(
        self,
        projectId: Optional[int],
        stepId: int,
        languageIds: Optional[str] = None,
        orderBy: Optional[Sorting] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ):
        """
        List Strings on the Workflow Step.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.workflow-steps.strings.getMany
        """
        projectId = projectId or self.get_project_id()

        params = {
            "languageIds": languageIds,
            "orderBy": orderBy,
            "status": status
        }
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_workflow_step_strings_path(projectId=projectId, stepId=stepId),
            params=params
        )
