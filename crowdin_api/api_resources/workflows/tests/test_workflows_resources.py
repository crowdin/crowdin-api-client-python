from unittest import mock

import pytest

from crowdin_api.api_resources import WorkflowsResource
from crowdin_api.api_resources.workflows.enums import ListWorkflowStepStringsOrderBy
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestWorkflowsResource:
    resource_class = WorkflowsResource

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
            ({"projectId": 1}, "projects/1/workflow-steps"),
            ({"projectId": 1, "stepId": 1}, "projects/1/workflow-steps/1"),
        ),
    )
    def test_get_workflow_steps_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_workflow_steps_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({}, "workflow-templates"),
            ({"templateId": 1}, "workflow-templates/1"),
        ),
    )
    def test_get_workflow_templates_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_workflow_templates_path(**incoming_data) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_workflow_steps(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_workflow_steps(projectId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_workflow_steps_path(projectId=1),
            params=None
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_workflow_step(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_workflow_step(projectId=1, stepId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_workflow_steps_path(projectId=1, stepId=2)
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {},
                {
                    "groupId": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "groupId": 1,
                    "offset": 0,
                    "limit": 25,
                },
                {
                    "groupId": 1,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_workflow_templates(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_workflow_templates(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_workflow_templates_path(),
            params=request_params
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_workflow_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_workflow_template(templateId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_workflow_templates_path(templateId=1)
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"projectId": 1, "stepId": 2},
                {
                    "languageIds": None,
                    "orderBy": None,
                    "status": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListWorkflowStepStringsOrderBy.ID, SortingOrder.DESC
                            )
                        ]
                    ),
                    "projectId": 1,
                    "stepId": 2,
                    "languageIds": "es,fr",
                    "status": "done",
                    "offset": 10,
                    "limit": 50,
                },
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListWorkflowStepStringsOrderBy.ID, SortingOrder.DESC
                            )
                        ]
                    ),
                    "languageIds": "es,fr",
                    "status": "done",
                    "offset": 10,
                    "limit": 50,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_workflow_step_strings(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_workflow_step_strings(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_workflow_step_strings_path(
                projectId=in_params["projectId"],
                stepId=in_params["stepId"]
            ),
            params=request_params
        )
