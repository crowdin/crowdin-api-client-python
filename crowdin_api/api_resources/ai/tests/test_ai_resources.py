from datetime import datetime, timezone
from unittest import mock

import pytest

from crowdin_api.api_resources.ai.enums import (
    AIPromptAction,
    AIProviderType,
    DatasetPurpose,
    AiPromptFineTuningJobStatus,
    ListAiPromptFineTuningJobsOrderBy,
    EditAiCustomPlaceholderPatchPath,
    AiToolType,
    AiReportFormat,
    EditAiSettingsPatchPath, ListSupportedAiModelsOrderBy
)
from crowdin_api.api_resources.ai.resource import AIResource, EnterpriseAIResource
from crowdin_api.api_resources.ai.types import (
    AIPromptOperation,
    EditAIPromptPath,
    CreateAIPromptFineTuningJobRequest,
    HyperParameters,
    TrainingOptions,
    GenerateAIPromptFineTuningDatasetRequest,
    GenerateAiPromptCompletionRequest,
    PreTranslateActionAiPromptContextResources,
    AiTool,
    AiToolObject,
    AiToolFunction,
    GenerateAiReportRequest,
    GeneralReportSchema
)
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingRule, SortingOrder


class TestAIResources:
    resource_class = AIResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

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
        "in_params, path",
        (
            ({"userId": 1}, "users/1/ai/providers"),
            ({"userId": 1, "aiProviderId": 2}, "users/1/ai/providers/2"),
        ),
    )
    def test_get_ai_provider_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_provider_path(**in_params) == path

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
                "op": AIPromptOperation.REPLACE,
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

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 20,
                    "offset": 2,
                },
                {
                    "limit": 20,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_providers(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        userId = 1
        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_providers(userId=userId, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_provider_path(userId=userId),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {"name": "basic", "type": AIProviderType.OPEN_AI},
                {"name": "basic", "type": AIProviderType.OPEN_AI},
            ),
            (
                {
                    "name": "basic",
                    "type": AIProviderType.OPEN_AI,
                    "credentials": {"apiKey": "test-api-key"},
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "enabledProjectIds": [1, 2, 3],
                    "config": {
                        "actionRules": [
                            {
                                "action": AIPromptAction.PRE_TRANSLATE,
                                "availableAiModelIds": ["gpt-3.5-turbo-instruct"],
                            }
                        ]
                    },
                    "isEnabled": True,
                    "useSystemCredentials": False,
                },
                {
                    "name": "basic",
                    "type": AIProviderType.OPEN_AI,
                    "credentials": {"apiKey": "test-api-key"},
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "enabledProjectIds": [1, 2, 3],
                    "config": {
                        "actionRules": [
                            {
                                "action": AIPromptAction.PRE_TRANSLATE,
                                "availableAiModelIds": ["gpt-3.5-turbo-instruct"],
                            }
                        ]
                    },
                    "isEnabled": True,
                    "useSystemCredentials": False,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_ai_provider(
        self, m_request, incoming_data, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        userId = 1
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.add_ai_provider(userId=userId, request_data=incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_ai_provider_path(userId=userId),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_provider(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiProviderId = 2
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_ai_provider(userId=userId, aiProviderId=aiProviderId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_provider_path(
                userId=userId, aiProviderId=aiProviderId
            ),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_ai_provider(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiProviderId = 2
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.delete_ai_provider(userId=userId, aiProviderId=aiProviderId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_ai_provider_path(
                userId=userId, aiProviderId=aiProviderId
            ),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_provider(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiProviderId = 2
        request_data = [
            {
                "op": AIPromptOperation.REPLACE,
                "path": EditAIPromptPath.NAME,
                "value": "test",
            }
        ]
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_ai_provider(
                userId=userId, aiProviderId=aiProviderId, request_data=request_data
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_ai_provider_path(
                userId=userId, aiProviderId=aiProviderId
            ),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_provider_models(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiProviderId = 2
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_ai_provider_models(userId=userId, aiProviderId=aiProviderId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_provider_path(userId=userId, aiProviderId=aiProviderId)
            + "/models",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_create_ai_proxy_chat_completion(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        userId = 1
        aiProviderId = 2
        request_data = {"model": "string", "stream": True}
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.create_ai_proxy_chat_completion(
                userId=userId, aiProviderId=aiProviderId, request_data=request_data
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_ai_provider_path(userId=userId, aiProviderId=aiProviderId)
            + "/chat/completions",
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                GenerateAIPromptFineTuningDatasetRequest(
                    projectIds=[1],
                    tmIds=[2, 3],
                    purpose=DatasetPurpose.TRAINING.value,
                    dateFrom=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                    dateTo=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                    maxFileSize=20,
                    minExamplesCount=2,
                    maxExamplesCount=10
                ),
                {
                    "projectIds": [
                        1
                    ],
                    "tmIds": [
                        2, 3
                    ],
                    "purpose": "training",
                    "dateFrom": "2019-09-23T11:26:54+00:00",
                    "dateTo": "2019-09-23T11:26:54+00:00",
                    "maxFileSize": 20,
                    "minExamplesCount": 2,
                    "maxExamplesCount": 10
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_ai_prompt_fine_tuning_dataset(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_ai_prompt_fine_tuning_dataset(user_id, ai_prompt_id, request_data=incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/datasets",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt_fine_tuning_dataset_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_ai_prompt_fine_tuning_dataset_generation_status(user_id, ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/datasets/{job_identifier}",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                CreateAIPromptFineTuningJobRequest(
                    dryRun=False,
                    hyperparameters=HyperParameters(
                        batchSize=1,
                        learningRateMultiplier=2.0,
                        nEpochs=100,
                    ),
                    trainingOptions=TrainingOptions(
                        projectIds=[1],
                        tmIds=[2],
                        dateFrom=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                        dateTo=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                        maxFileSize=10,
                        minExamplesCount=200,
                        maxExamplesCount=300
                    )
                ),
                {
                    "dryRun": False,
                    "hyperparameters": {
                        "batchSize": 1,
                        "learningRateMultiplier": 2.0,
                        "nEpochs": 100,
                    },
                    "trainingOptions": {
                        "projectIds": [1],
                        "tmIds": [2],
                        "dateFrom": "2019-09-23T11:26:54+00:00",
                        "dateTo": "2019-09-23T11:26:54+00:00",
                        "maxFileSize": 10,
                        "minExamplesCount": 200,
                        "maxExamplesCount": 300
                    }
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_create_ai_prompt_fine_tuning_job(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.create_ai_prompt_fine_tuning_job(user_id, ai_prompt_id, request_data=incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/jobs",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt_fine_tuning_job_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_ai_prompt_fine_tuning_job_status(user_id, ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_ai_prompt_fine_tuning_dataset(
        self,
        m_request,
        base_absolut_url
    ):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.download_ai_prompt_fine_tuning_dataset(user_id, ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/datasets/{job_identifier}/download",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_prompt_fine_tuning_events(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_ai_prompt_fine_tuning_events(user_id, ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}/events",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "statuses": None,
                    "orderBy": None,
                    "limit": None,
                    "offset": None,
                },
            ),
            (
                {
                    "statuses": [
                        AiPromptFineTuningJobStatus.CREATED,
                        AiPromptFineTuningJobStatus.IN_PROGRESS,
                        AiPromptFineTuningJobStatus.FINISHED
                    ],
                    "order_by": Sorting([
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.UPDATED_AT, SortingOrder.DESC),
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.STARTED_AT, SortingOrder.DESC)
                    ]),
                    "limit": 10,
                    "offset": 2
                },
                {
                    "statuses": "created,in_progress,finished",
                    "orderBy": Sorting([
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.UPDATED_AT, SortingOrder.DESC),
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.STARTED_AT, SortingOrder.DESC)
                    ]),
                    "limit": 10,
                    "offset": 2
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_prompt_fine_tuning_jobs(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_prompt_fine_tuning_jobs(user_id, **incoming_data) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/prompts/fine-tuning/jobs",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_custom_placeholders(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_custom_placeholders(user_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/settings/custom-placeholders",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {
                    "description": "Product description",
                    "placeholder": "%custom:productDescription%",
                    "value": "The product is the professional consulting service"
                },
                {
                    "description": "Product description",
                    "placeholder": "%custom:productDescription%",
                    "value": "The product is the professional consulting service"
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_ai_custom_placeholder(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.add_ai_custom_placeholder(user_id, incoming_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path=f"users/{user_id}/ai/settings/custom-placeholders",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_custom_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_custom_placeholder_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_custom_placeholder(user_id, ai_custom_placeholder_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/settings/custom-placeholders/{ai_custom_placeholder_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_ai_custom_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_custom_placeholder_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_ai_custom_placeholder(user_id, ai_custom_placeholder_id) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path=f"users/{user_id}/ai/settings/custom-placeholders/{ai_custom_placeholder_id}",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                [
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiCustomPlaceholderPatchPath.DESCRIPTION.value,
                        "value": "New description"
                    },
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiCustomPlaceholderPatchPath.VALUE.value,
                        "value": "The product is the professional consulting service"
                    }
                ],
                [
                    {
                        "op": "replace",
                        "path": "/description",
                        "value": "New description"
                    },
                    {
                        "op": "replace",
                        "path": "/value",
                        "value": "The product is the professional consulting service"
                    }
                ],
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_custom_placeholder(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_custom_placeholder_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_ai_custom_placeholder(user_id, ai_custom_placeholder_id, incoming_data) == "response"

        m_request.assert_called_once_with(
            method="patch",
            path=f"users/{user_id}/ai/settings/custom-placeholders/{ai_custom_placeholder_id}",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_clone_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        name = "name"

        resource = self.get_resource(base_absolut_url)
        assert resource.clone_ai_prompt(user_id, ai_prompt_id, name) == "response"

        m_request.assert_called_once_with(
            method="post",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/clones",
            request_data={
                "name": name
            },
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                GenerateAiPromptCompletionRequest(
                    resources=PreTranslateActionAiPromptContextResources(
                        projectId=1,
                        sourceLanguageId="en",
                        targetLanguageId="uk",
                        stringIds=[1, 2, 3],
                        overridePromptValues={
                            "property1": "string"
                        }
                    ),
                    tools=[
                        AiToolObject(
                            tool=AiTool(
                                type=AiToolType.FUNCTION.value,
                                function=AiToolFunction(
                                    name="Name",
                                    description="Description",
                                    parameters={}
                                )
                            )
                        )
                    ],
                    tool_choice="string"
                ),
                {
                    "resources": {
                        "projectId": 1,
                        "sourceLanguageId": "en",
                        "targetLanguageId": "uk",
                        "stringIds": [1, 2, 3],
                        "overridePromptValues": {
                            "property1": "string"
                        }
                    },
                    "tools": [
                        {
                            "tool": {
                                "type": "function",
                                "function": {
                                    "name": "Name",
                                    "description": "Description",
                                    "parameters": {}
                                }
                            }
                        }
                    ],
                    "tool_choice": "string"
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_ai_prompt_completion(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_ai_prompt_completion(user_id, ai_prompt_id, incoming_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/completions",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt_completion_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        completion_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_prompt_completion_status(user_id, ai_prompt_id, completion_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/completions/{completion_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_cancel_ai_prompt_completion(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        completion_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.cancel_ai_prompt_completion(user_id, ai_prompt_id, completion_id) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/completions/{completion_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_ai_prompt_completion(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_prompt_id = 2
        completion_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_ai_prompt_completion(user_id, ai_prompt_id, completion_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/completions/{completion_id}/download",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                GenerateAiReportRequest(
                    type="tokens-usage-raw-data",
                    schema=GeneralReportSchema(
                        dateFrom=datetime(2024, 1, 23, 7, 0, 14, tzinfo=timezone.utc).isoformat(),
                        dateTo=datetime(2024, 9, 27, 7, 0, 14, tzinfo=timezone.utc).isoformat(),
                        format=AiReportFormat.JSON.value,
                        projectIds=[1, 2, 3],
                        promptIds=[4, 5, 6],
                        userIds=[7, 8, 9]
                    )
                ),
                {
                    "type": "tokens-usage-raw-data",
                    "schema": {
                        "dateFrom": "2024-01-23T07:00:14+00:00",
                        "dateTo": "2024-09-27T07:00:14+00:00",
                        "format": "json",
                        "projectIds": [1, 2, 3],
                        "promptIds": [4, 5, 6],
                        "userIds": [7, 8, 9]
                    }
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_ai_report(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_ai_report(user_id, incoming_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path=f"users/{user_id}/ai/reports",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_ai_report_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_report_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_ai_report_generation_status(user_id, ai_report_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/reports/{ai_report_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_ai_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1
        ai_report_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_ai_report(user_id, ai_report_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/reports/{ai_report_id}/download",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_settings(user_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/settings",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                [
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiSettingsPatchPath.ASSIST_ACTION_AI_PROMPT_ID.value,
                        "value": 1
                    },
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiSettingsPatchPath.EDITOR_SUGGESTION_AI_PROMPT_ID.value,
                        "value": 2
                    }
                ],
                [
                    {
                        "op": "replace",
                        "path": "/assistActionAiPromptId",
                        "value": 1
                    },
                    {
                        "op": "replace",
                        "path": "/editorSuggestionAiPromptId",
                        "value": 2
                    }
                ],
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_settings(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_ai_settings(user_id, incoming_data) == "response"

        m_request.assert_called_once_with(
            method="patch",
            path=f"users/{user_id}/ai/settings",
            request_data=request_params,
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "limit": 25,
                    "offset": 0,
                    "provider_type": AIProviderType.OPEN_AI,
                    "enabled": True,
                    "order_by": Sorting([
                        SortingRule(ListSupportedAiModelsOrderBy.KNOWLEDGE_CUTOFF, SortingOrder.DESC)
                    ])
                },
                {
                    "limit": 25,
                    "offset": 0,
                    "providerType": "open_ai",
                    "enabled": True,
                    "orderBy": "knowledgeCutoff desc",
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_supported_ai_provider_models(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        user_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.list_supported_ai_provider_models(user_id, **in_params) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"users/{user_id}/ai/providers/supported-models",
            params=request_params
        )



class TestEnterpriseAIResources:
    resource_class = EnterpriseAIResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "ai/prompts"),
            ({"aiPromptId": 1}, "ai/prompts/1"),
        ),
    )
    def test_get_ai_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "ai/providers"),
            ({"aiProviderId": 1}, "ai/providers/1"),
        ),
    )
    def test_get_ai_provider_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_provider_path(**in_params) == path

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

        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_prompts(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_path(),
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
                    "config": {
                        "mode": "advanced",
                        "prompt": "test prompt",
                        "screenshot": True,
                    },
                },
                {
                    "name": "basic",
                    "action": AIPromptAction.ASSIST,
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "isEnabled": False,
                    "enabledProjectIds": [1, 2, 3],
                    "config": {
                        "mode": "advanced",
                        "prompt": "test prompt",
                        "screenshot": True,
                    },
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_ai_prompt(
        self, m_request, incoming_data, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_ai_prompt(request_data=incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_ai_path(),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiPromptId = 1
        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_prompt(aiPromptId=aiPromptId) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_path(aiPromptId=aiPromptId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiPromptId = 1
        resource = self.get_resource(base_absolut_url)
        assert resource.delete_ai_prompt(aiPromptId=aiPromptId) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_ai_path(aiPromptId=aiPromptId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiPromptId = 1
        request_data = [
            {
                "op": AIPromptOperation.REPLACE,
                "path": EditAIPromptPath.NAME,
                "value": "test",
            }
        ]
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_ai_prompt(aiPromptId=aiPromptId, request_data=request_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_ai_path(aiPromptId=aiPromptId),
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 20,
                    "offset": 2,
                },
                {
                    "limit": 20,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_providers(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_providers(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_provider_path(),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {"name": "basic", "type": AIProviderType.OPEN_AI},
                {"name": "basic", "type": AIProviderType.OPEN_AI},
            ),
            (
                {
                    "name": "basic",
                    "type": AIProviderType.OPEN_AI,
                    "credentials": {"apiKey": "test-api-key"},
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "enabledProjectIds": [1, 2, 3],
                    "config": {
                        "actionRules": [
                            {
                                "action": AIPromptAction.PRE_TRANSLATE,
                                "availableAiModelIds": ["gpt-3.5-turbo-instruct"],
                            }
                        ]
                    },
                    "isEnabled": True,
                    "useSystemCredentials": False,
                },
                {
                    "name": "basic",
                    "type": AIProviderType.OPEN_AI,
                    "credentials": {"apiKey": "test-api-key"},
                    "aiProviderId": 1,
                    "aiModelId": "gpt-3.5-turbo-instruct",
                    "enabledProjectIds": [1, 2, 3],
                    "config": {
                        "actionRules": [
                            {
                                "action": AIPromptAction.PRE_TRANSLATE,
                                "availableAiModelIds": ["gpt-3.5-turbo-instruct"],
                            }
                        ]
                    },
                    "isEnabled": True,
                    "useSystemCredentials": False,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_ai_provider(
        self, m_request, incoming_data, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_ai_provider(request_data=incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_ai_provider_path(),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_provider(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiProviderId = 1
        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_provider(aiProviderId=aiProviderId) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_provider_path(aiProviderId=aiProviderId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_ai_provider(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiProviderId = 1
        resource = self.get_resource(base_absolut_url)
        assert resource.delete_ai_provider(aiProviderId=aiProviderId) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_ai_provider_path(aiProviderId=aiProviderId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_provider(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiProviderId = 1
        request_data = [
            {
                "op": AIPromptOperation.REPLACE,
                "path": EditAIPromptPath.NAME,
                "value": "test",
            }
        ]
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.edit_ai_provider(
                aiProviderId=aiProviderId, request_data=request_data
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_ai_provider_path(aiProviderId=aiProviderId),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_provider_models(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiProviderId = 1
        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_provider_models(aiProviderId=aiProviderId) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_ai_provider_path(aiProviderId=aiProviderId) + "/models",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_create_ai_proxy_chat_completion(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        aiProviderId = 1
        request_data = {"model": "string", "stream": True}
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.create_ai_proxy_chat_completion(
                aiProviderId=aiProviderId, request_data=request_data
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_ai_provider_path(aiProviderId=aiProviderId)
            + "/chat/completions",
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                GenerateAIPromptFineTuningDatasetRequest(
                    projectIds=[1],
                    tmIds=[2, 3],
                    purpose=DatasetPurpose.TRAINING.value,
                    dateFrom=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                    dateTo=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                    maxFileSize=20,
                    minExamplesCount=2,
                    maxExamplesCount=10
                ),
                {
                    "projectIds": [1],
                    "tmIds": [2, 3],
                    "purpose": "training",
                    "dateFrom": "2019-09-23T11:26:54+00:00",
                    "dateTo": "2019-09-23T11:26:54+00:00",
                    "maxFileSize": 20,
                    "minExamplesCount": 2,
                    "maxExamplesCount": 10
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_ai_prompt_fine_tuning_dataset(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_ai_prompt_fine_tuning_dataset(ai_prompt_id, request_data=incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=f"ai/prompts/{ai_prompt_id}/fine-tuning/datasets",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt_fine_tuning_dataset_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_ai_prompt_fine_tuning_dataset_generation_status(ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"ai/prompts/{ai_prompt_id}/fine-tuning/datasets/{job_identifier}",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                CreateAIPromptFineTuningJobRequest(
                    dryRun=False,
                    hyperparameters=HyperParameters(
                        batchSize=1,
                        learningRateMultiplier=2.0,
                        nEpochs=100,
                    ),
                    trainingOptions=TrainingOptions(
                        projectIds=[1],
                        tmIds=[2],
                        dateFrom=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                        dateTo=datetime(2019, 9, 23, 11, 26, 54, tzinfo=timezone.utc).isoformat(),
                        maxFileSize=10,
                        minExamplesCount=200,
                        maxExamplesCount=300
                    )
                ),
                {
                    "dryRun": False,
                    "hyperparameters": {
                        "batchSize": 1,
                        "learningRateMultiplier": 2.0,
                        "nEpochs": 100,
                    },
                    "trainingOptions": {
                        "projectIds": [1],
                        "tmIds": [2],
                        "dateFrom": "2019-09-23T11:26:54+00:00",
                        "dateTo": "2019-09-23T11:26:54+00:00",
                        "maxFileSize": 10,
                        "minExamplesCount": 200,
                        "maxExamplesCount": 300
                    }
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_create_ai_prompt_fine_tuning_job(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.create_ai_prompt_fine_tuning_job(ai_prompt_id, request_data=incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=f"ai/prompts/{ai_prompt_id}/fine-tuning/jobs",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt_fine_tuning_job_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_ai_prompt_fine_tuning_job_status(ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_ai_prompt_fine_tuning_dataset(
            self,
            m_request,
            base_absolut_url
    ):
        m_request.return_value = "response"

        ai_prompt_id = 1
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.download_ai_prompt_fine_tuning_dataset(ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"ai/prompts/{ai_prompt_id}/fine-tuning/datasets/{job_identifier}/download",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_prompt_fine_tuning_events(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1
        job_identifier = "id"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_ai_prompt_fine_tuning_events(ai_prompt_id, job_identifier)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=f"ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}/events",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "statuses": None,
                    "orderBy": None,
                    "limit": None,
                    "offset": None,
                },
            ),
            (
                {
                    "statuses": [
                        AiPromptFineTuningJobStatus.CREATED,
                        AiPromptFineTuningJobStatus.IN_PROGRESS,
                        AiPromptFineTuningJobStatus.FINISHED
                    ],
                    "order_by": Sorting([
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.UPDATED_AT, SortingOrder.DESC),
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.STARTED_AT, SortingOrder.DESC)
                    ]),
                    "limit": 10,
                    "offset": 2
                },
                {
                    "statuses": "created,in_progress,finished",
                    "orderBy": Sorting([
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.UPDATED_AT, SortingOrder.DESC),
                        SortingRule(ListAiPromptFineTuningJobsOrderBy.STARTED_AT, SortingOrder.DESC)
                    ]),
                    "limit": 10,
                    "offset": 2
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_prompt_fine_tuning_jobs(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_prompt_fine_tuning_jobs(**incoming_data) == "response"

        m_request.assert_called_once_with(
            method="get",
            path="ai/prompts/fine-tuning/jobs",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_ai_custom_placeholders(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_ai_custom_placeholders() == "response"

        m_request.assert_called_once_with(
            method="get",
            path="ai/settings/custom-placeholders",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {
                    "description": "Product description",
                    "placeholder": "%custom:productDescription%",
                    "value": "The product is the professional consulting service"
                },
                {
                    "description": "Product description",
                    "placeholder": "%custom:productDescription%",
                    "value": "The product is the professional consulting service"
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_ai_custom_placeholder(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_ai_custom_placeholder(incoming_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path="ai/settings/custom-placeholders",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_custom_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_custom_placeholder_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_custom_placeholder(ai_custom_placeholder_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"ai/settings/custom-placeholders/{ai_custom_placeholder_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_ai_custom_placeholder(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_custom_placeholder_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_ai_custom_placeholder(ai_custom_placeholder_id) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path=f"ai/settings/custom-placeholders/{ai_custom_placeholder_id}",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                [
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiCustomPlaceholderPatchPath.DESCRIPTION.value,
                        "value": "New description"
                    },
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiCustomPlaceholderPatchPath.VALUE.value,
                        "value": "The product is the professional consulting service"
                    }
                ],
                [
                    {
                        "op": "replace",
                        "path": "/description",
                        "value": "New description"
                    },
                    {
                        "op": "replace",
                        "path": "/value",
                        "value": "The product is the professional consulting service"
                    }
                ],
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_custom_placeholder(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        ai_custom_placeholder_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_ai_custom_placeholder(ai_custom_placeholder_id, incoming_data) == "response"

        m_request.assert_called_once_with(
            method="patch",
            path=f"ai/settings/custom-placeholders/{ai_custom_placeholder_id}",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_clone_ai_prompt(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1
        name = "name"

        resource = self.get_resource(base_absolut_url)
        assert resource.clone_ai_prompt(ai_prompt_id, name) == "response"

        m_request.assert_called_once_with(
            method="post",
            path=f"ai/prompts/{ai_prompt_id}/clones",
            request_data={
                "name": name
            },
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                GenerateAiPromptCompletionRequest(
                    resources=PreTranslateActionAiPromptContextResources(
                        projectId=1,
                        sourceLanguageId="en",
                        targetLanguageId="uk",
                        stringIds=[1, 2, 3],
                        overridePromptValues={
                            "property1": "string"
                        }
                    ),
                    tools=[
                        AiToolObject(
                            tool=AiTool(
                                type=AiToolType.FUNCTION.value,
                                function=AiToolFunction(
                                    name="Name",
                                    description="Description",
                                    parameters={}
                                )
                            )
                        )
                    ],
                    tool_choice="string"
                ),
                {
                    "resources": {
                        "projectId": 1,
                        "sourceLanguageId": "en",
                        "targetLanguageId": "uk",
                        "stringIds": [1, 2, 3],
                        "overridePromptValues": {
                            "property1": "string"
                        }
                    },
                    "tools": [
                        {
                            "tool": {
                                "type": "function",
                                "function": {
                                    "name": "Name",
                                    "description": "Description",
                                    "parameters": {}
                                }
                            }
                        }
                    ],
                    "tool_choice": "string"
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_ai_prompt_completion(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_ai_prompt_completion(ai_prompt_id, incoming_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path=f"ai/prompts/{ai_prompt_id}/completions",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_prompt_completion_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1
        completion_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_prompt_completion_status(ai_prompt_id, completion_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"ai/prompts/{ai_prompt_id}/completions/{completion_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_cancel_ai_prompt_completion(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1
        completion_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.cancel_ai_prompt_completion(ai_prompt_id, completion_id) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path=f"ai/prompts/{ai_prompt_id}/completions/{completion_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_ai_prompt_completion(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_prompt_id = 1
        completion_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_ai_prompt_completion(ai_prompt_id, completion_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"ai/prompts/{ai_prompt_id}/completions/{completion_id}/download",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                GenerateAiReportRequest(
                    type="tokens-usage-raw-data",
                    schema=GeneralReportSchema(
                        dateFrom=datetime(2024, 1, 23, 7, 0, 14, tzinfo=timezone.utc).isoformat(),
                        dateTo=datetime(2024, 9, 27, 7, 0, 14, tzinfo=timezone.utc).isoformat(),
                        format=AiReportFormat.JSON.value,
                        projectIds=[1, 2, 3],
                        promptIds=[4, 5, 6],
                        userIds=[7, 8, 9]
                    )
                ),
                {
                    "type": "tokens-usage-raw-data",
                    "schema": {
                        "dateFrom": "2024-01-23T07:00:14+00:00",
                        "dateTo": "2024-09-27T07:00:14+00:00",
                        "format": "json",
                        "projectIds": [1, 2, 3],
                        "promptIds": [4, 5, 6],
                        "userIds": [7, 8, 9]
                    }
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_ai_report(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_ai_report(incoming_data) == "response"

        m_request.assert_called_once_with(
            method="post",
            path="ai/reports",
            request_data=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_ai_report_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_report_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_ai_report_generation_status(ai_report_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"ai/reports/{ai_report_id}",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_ai_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        ai_report_id = "id"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_ai_report(ai_report_id) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"ai/reports/{ai_report_id}/download",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_ai_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_ai_settings() == "response"

        m_request.assert_called_once_with(
            method="get",
            path="ai/settings",
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                [
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiSettingsPatchPath.ASSIST_ACTION_AI_PROMPT_ID.value,
                        "value": 1
                    },
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": EditAiSettingsPatchPath.EDITOR_SUGGESTION_AI_PROMPT_ID.value,
                        "value": 2
                    }
                ],
                [
                    {
                        "op": "replace",
                        "path": "/assistActionAiPromptId",
                        "value": 1
                    },
                    {
                        "op": "replace",
                        "path": "/editorSuggestionAiPromptId",
                        "value": 2
                    }
                ],
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_ai_settings(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_ai_settings(incoming_data) == "response"

        m_request.assert_called_once_with(
            method="patch",
            path="ai/settings",
            request_data=request_params,
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "limit": 25,
                    "offset": 0,
                    "provider_type": AIProviderType.OPEN_AI,
                    "enabled": True,
                    "order_by": Sorting([
                        SortingRule(ListSupportedAiModelsOrderBy.KNOWLEDGE_CUTOFF, SortingOrder.DESC)
                    ])
                },
                {
                    "limit": 25,
                    "offset": 0,
                    "providerType": "open_ai",
                    "enabled": True,
                    "orderBy": "knowledgeCutoff desc",
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_supported_ai_provider_models(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_supported_ai_provider_models(**in_params) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=f"ai/providers/supported-models",
            params=request_params
        )
