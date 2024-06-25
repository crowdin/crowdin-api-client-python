from unittest import mock

import pytest
from crowdin_api.api_resources.ai.enums import AIPromptAction
from crowdin_api.api_resources.ai.resource import AIResource
from crowdin_api.api_resources.ai.types import EditAIPromptOperation, EditAIPromptPath
from crowdin_api.requester import APIRequester


class TestAIResources:
    resource_class = AIResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"userId": 1}, "users/1/ai/prompts"),
            ({"userId": 1, "aiPromptId": 2}, "users/1/ai/prompts/2"),
        ),
    )
    def test_get_ai_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_path(**in_params) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "projectId": None,
                    "action": None,
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "projectId": 1,
                    "action": AIPromptAction.ASSIST,
                    "limit": 20,
                    "offset": 2,
                },
                {
                    "projectId": 1,
                    "action": AIPromptAction.ASSIST,
                    "limit": 20,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_prompts(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        userId = 1
        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_prompts(userId=userId, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_path(userId=userId),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "name": "basic",
                    "action": AIPromptAction.ASSIST,
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "config": {"mode": "advanced", "prompt": "test prompt"},
                },
                {
                    "name": "basic",
                    "action": AIPromptAction.ASSIST,
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "config": {"mode": "advanced", "prompt": "test prompt"},
                },
            ),
            (
                {
                    "name": "basic",
                    "action": AIPromptAction.ASSIST,
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "isEnabled": False,
                    "enabledProjectIds": [1, 2, 3],
                    "config": {"mode": "advanced", "prompt": "test prompt"},
                },
                {
                    "name": "basic",
                    "action": AIPromptAction.ASSIST,
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "isEnabled": False,
                    "enabledProjectIds": [1, 2, 3],
                    "config": {"mode": "advanced", "prompt": "test prompt"},
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_ai_prompt(
        self, m_request, incoming_data, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        userId = 1
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_ai_prompt(userId=userId, request_data=incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_ai_path(userId=userId),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiPromptId = 2
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_ai_prompt(userId=userId, aiPromptId=aiPromptId) == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_path(userId=userId, aiPromptId=aiPromptId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiPromptId = 2
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.delete_ai_prompt(userId=userId, aiPromptId=aiPromptId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_ai_path(userId=userId, aiPromptId=aiPromptId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiPromptId = 2
        request_data = [
            {
                "op": EditAIPromptOperation.REPLACE,
                "path": EditAIPromptPath.NAME,
                "value": "test",
            }
        ]
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_ai_prompt(
                userId=userId, aiPromptId=aiPromptId, request_data=request_data
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_ai_path(userId=userId, aiPromptId=aiPromptId),
            request_data=request_data,
        )
