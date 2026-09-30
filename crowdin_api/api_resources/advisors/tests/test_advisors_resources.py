from unittest import mock

import pytest

from crowdin_api.api_resources.advisors.enums import (
    AdvisorInspectorMode,
    AdvisorInsightMetricSource,
    AdvisorInsightMetricTone,
    AdvisorInsightMetricUnit,
    AdvisorInsightOutcome,
    AdvisorInsightPatchPath,
    AdvisorInsightStatus,
)
from crowdin_api.api_resources.advisors.resource import AdvisorsResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.requester import APIRequester


class TestAdvisorsResource:
    resource_class = AdvisorsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/advisors/checks"),
            ({"projectId": 1, "checkId": "abc"}, "projects/1/advisors/checks/abc"),
        ),
    )
    def test_get_advisor_checks_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_advisor_checks_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/advisors/insights"),
            ({"projectId": 1, "insightId": 2}, "projects/1/advisors/insights/2"),
        ),
    )
    def test_get_advisor_insights_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_advisor_insights_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            ({}, {"category": None, "inspectors": None}),
            ({"category": "strings"}, {"category": "strings", "inspectors": None}),
            (
                {
                    "inspectors": [
                        {
                            "key": "string_context_relevance",
                            "options": {"mode": AdvisorInspectorMode.AUTO, "promptId": 3},
                        }
                    ]
                },
                {
                    "category": None,
                    "inspectors": [
                        {
                            "key": "string_context_relevance",
                            "options": {"mode": AdvisorInspectorMode.AUTO, "promptId": 3},
                        }
                    ],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_create_advisor_check(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.create_advisor_check(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/advisors/checks",
            request_data=request_data,
        )

    def test_create_advisor_check_invalid(self, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        with pytest.raises(ValueError):
            resource.create_advisor_check(
                category="strings", inspectors=[{"key": "k"}], projectId=1
            )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_advisor_check_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_advisor_check_status("abc", projectId=1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/advisors/checks/abc",
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {},
                {
                    "isDismissed": None,
                    "status": None,
                    "outcome": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
            (
                {
                    "isDismissed": False,
                    "status": [AdvisorInsightStatus.DONE, "outdated"],
                    "outcome": AdvisorInsightOutcome.FLAGGED,
                    "offset": 10,
                    "limit": 5,
                },
                {
                    "isDismissed": False,
                    "status": "done,outdated",
                    "outcome": AdvisorInsightOutcome.FLAGGED,
                    "offset": 10,
                    "limit": 5,
                },
            ),
            (
                {"status": "pending,checking"},
                {
                    "isDismissed": None,
                    "status": "pending,checking",
                    "outcome": None,
                    "offset": 0,
                    "limit": 25,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_advisor_insights(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_advisor_insights(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/1/advisors/insights",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_advisor_insight(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        data = [
            {
                "op": PatchOperation.REPLACE,
                "path": AdvisorInsightPatchPath.IS_DISMISSED,
                "value": True,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_advisor_insight(2, data, projectId=1) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path="projects/1/advisors/insights/2",
            request_data=data,
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"outcome": AdvisorInsightOutcome.CLEAR},
                {
                    "outcome": AdvisorInsightOutcome.CLEAR,
                    "checkedAt": None,
                    "metrics": None,
                    "recommendations": None,
                    "payload": None,
                },
            ),
            (
                {
                    "outcome": AdvisorInsightOutcome.FLAGGED,
                    "checkedAt": "2026-01-01T00:00:00+00:00",
                    "metrics": [
                        {
                            "key": "quality_score",
                            "value": 12,
                            "unit": AdvisorInsightMetricUnit.PERCENT,
                            "tone": AdvisorInsightMetricTone.DANGER,
                            "source": AdvisorInsightMetricSource.APP,
                        }
                    ],
                    "recommendations": [{"id": "r1", "primary": True, "params": {"a": 1}}],
                    "payload": {"x": "y"},
                },
                {
                    "outcome": AdvisorInsightOutcome.FLAGGED,
                    "checkedAt": "2026-01-01T00:00:00+00:00",
                    "metrics": [
                        {
                            "key": "quality_score",
                            "value": 12,
                            "unit": AdvisorInsightMetricUnit.PERCENT,
                            "tone": AdvisorInsightMetricTone.DANGER,
                            "source": AdvisorInsightMetricSource.APP,
                        }
                    ],
                    "recommendations": [{"id": "r1", "primary": True, "params": {"a": 1}}],
                    "payload": {"x": "y"},
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_create_or_update_application_advisor_insight(
        self, m_request, in_params, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.create_or_update_application_advisor_insight(
                "my-app", "my-module", projectId=1, **in_params
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="put",
            path="projects/1/applications/my-app/modules/my-module/advisors/insights",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_default_project_id(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=5
        )
        assert resource.get_advisor_check_status("abc") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="projects/5/advisors/checks/abc",
        )
