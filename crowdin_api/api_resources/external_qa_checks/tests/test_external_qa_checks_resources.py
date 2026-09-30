from unittest import mock

import pytest

from crowdin_api.api_resources.external_qa_checks.resource import ExternalQaChecksResource
from crowdin_api.requester import APIRequester


class TestExternalQaChecksResource:
    resource_class = ExternalQaChecksResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "external-qa-checks"),
            ({"externalQaCheckId": 1}, "external-qa-checks/1"),
        ),
    )
    def test_get_external_qa_checks_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_external_qa_checks_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            ({}, {"projectId": None, "offset": 0, "limit": 25}),
            (
                {"projectId": 1, "offset": 10, "limit": 5},
                {"projectId": 1, "offset": 10, "limit": 5},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_external_qa_checks(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_external_qa_checks(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="external-qa-checks",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_external_qa_check(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_external_qa_check(externalQaCheckId=1) == "response"
        m_request.assert_called_once_with(method="get", path="external-qa-checks/1")
