from typing import Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.ai.enums import AIPromptAction, AiPromptFineTuningJobStatus
from crowdin_api.api_resources.ai.types import (
    AddAIPromptRequestScheme,
    AddAIProviderReqeustScheme,
    EditAIPromptScheme,
    EditAIProviderRequestScheme,
    GoogleGeminiChatProxy,
    OtherChatProxy,
    GenerateAIPromptFineTuningDatasetRequest,
    CreateAIPromptFineTuningJobRequest,
    AddAiCustomPlaceholderRequest,
    EditAiCustomPlaceholderPatch,
    GenerateAiPromptCompletionRequest,
    GenerateAiReportRequest,
    EditAiSettingsPatch,
)
from crowdin_api.sorting import Sorting
from crowdin_api.utils import convert_enum_collection_to_string_if_exists


class AIResource(BaseResource):
    """
    Resource for AI.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/AI
    """

    def get_ai_path(self, userId: int, aiPromptId: Optional[int] = None):
        if aiPromptId is not None:
            return f"users/{userId}/ai/prompts/{aiPromptId}"
        return f"users/{userId}/ai/prompts"

    def get_ai_provider_path(self, userId: int, aiProviderId: Optional[int] = None):
        if aiProviderId is not None:
            return f"users/{userId}/ai/providers/{aiProviderId}"
        return f"users/{userId}/ai/providers"

    def list_ai_prompts(
        self,
        userId: int,
        projectId: Optional[int] = None,
        action: Optional[AIPromptAction] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List AI Prompts

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.ai.prompts.getMany
        """
        params = {"projectId": projectId, "action": action}
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self.requester.request(
            method="get", path=self.get_ai_path(userId=userId), params=params
        )

    def add_ai_prompt(self, userId: int, request_data: AddAIPromptRequestScheme):
        """
        Add AI Prompt

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.prompts.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_path(userId=userId),
            request_data=request_data,
        )

    def get_ai_prompt(self, userId: int, aiPromptId: int):
        """
        Get AI Prompt

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.prompts.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_path(userId=userId, aiPromptId=aiPromptId),
        )

    def delete_ai_prompt(self, userId: int, aiPromptId: int):
        """
        Delete AI Prompt

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.prompts.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_ai_path(userId=userId, aiPromptId=aiPromptId),
        )

    def edit_ai_prompt(
        self, userId: int, aiPromptId: int, request_data: Iterable[EditAIPromptScheme]
    ):
        """
        Edit AI Prompt

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.prompts.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_ai_path(userId=userId, aiPromptId=aiPromptId),
            request_data=request_data,
        )

    def list_ai_providers(
        self,
        userId: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List AI Providers

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.ai.providers.getMany
        """
        params = self.get_page_params(limit=limit, offset=offset)
        return self.requester.request(
            method="get", path=self.get_ai_provider_path(userId=userId), params=params
        )

    def add_ai_provider(self, userId: int, request_data: AddAIProviderReqeustScheme):
        """
        Add AI Provider

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.providers.post
        """
        return self.requester.request(
            method="post",
            path=self.get_ai_provider_path(userId=userId),
            request_data=request_data,
        )

    def get_ai_provider(self, userId: int, aiProviderId: int):
        """
        Get AI Provider

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.providers.get
        """
        return self.requester.request(
            method="get",
            path=self.get_ai_provider_path(userId=userId, aiProviderId=aiProviderId),
        )

    def delete_ai_provider(self, userId: int, aiProviderId: int):
        """
        Delete AI Provider

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.providers.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_ai_provider_path(userId=userId, aiProviderId=aiProviderId),
        )

    def edit_ai_provider(
        self, userId: int, aiProviderId: int, request_data: EditAIProviderRequestScheme
    ):
        """
        Edit AI Provider

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.providers.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_ai_provider_path(userId=userId, aiProviderId=aiProviderId),
            request_data=request_data,
        )

    def list_ai_provider_models(self, userId: int, aiProviderId: int):
        """
        List AI Provider Models

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.ai.providers.models.getMany
        """
        return self.requester.request(
            method="get",
            path=self.get_ai_provider_path(userId=userId, aiProviderId=aiProviderId)
            + "/models",
        )

    def create_ai_proxy_chat_completion(
        self,
        userId: int,
        aiProviderId: int,
        request_data: Union[GoogleGeminiChatProxy, OtherChatProxy],
    ):
        """
        Create AI Proxy Chat Completion

        This API method serves as an intermediary, forwarding your requests directly to the selected provider.
        Please refer to the documentation for the specific provider you use to determine the required payload format.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.users.ai.providers.chat.completions.post
        """
        return self.requester.request(
            method="post",
            path=self.get_ai_provider_path(userId=userId, aiProviderId=aiProviderId)
            + "/chat/completions",
            request_data=request_data,
        )

    def get_ai_prompt_fine_tuning_datasets_path(
        self,
        user_id: int,
        ai_prompt_id: Optional[int] = None,
        job_identifier: Optional[str] = None
    ):
        if job_identifier is not None:
            return f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/datasets/{job_identifier}"
        return f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/datasets"

    def get_ai_prompt_fine_tuning_jobs_path(
        self,
        user_id: int,
        ai_prompt_id: Optional[int] = None,
        job_identifier: Optional[str] = None
    ):
        if job_identifier is not None:
            return f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}"
        return f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/jobs"

    def generate_ai_prompt_fine_tuning_dataset(
        self,
        user_id: int,
        ai_prompt_id: int,
        request_data: GenerateAIPromptFineTuningDatasetRequest,
    ):
        """
        Generate AI Prompt Fine-Tuning Dataset

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.datasets.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_prompt_fine_tuning_datasets_path(user_id, ai_prompt_id),
            request_data=request_data,
        )

    def get_ai_prompt_fine_tuning_dataset_generation_status(
        self,
        user_id: int,
        ai_prompt_id: int,
        job_identifier: str
    ):
        """
        Get AI Prompt Fine-Tuning Dataset Generation Status

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.prompts.fine-tuning.datasets.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_fine_tuning_datasets_path(user_id, ai_prompt_id, job_identifier),
        )

    def list_ai_prompt_fine_tuning_events(
        self,
        user_id: int,
        ai_prompt_id: int,
        job_identifier: str,
    ):
        """
        List AI Prompt Fine-Tuning Events

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.jobs.events.getMany
        """

        return self.requester.request(
            method="get",
            path=f"users/{user_id}/ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}/events",
        )

    def list_ai_prompt_fine_tuning_jobs(
        self,
        user_id: int,
        statuses: Optional[Iterable[AiPromptFineTuningJobStatus]] = None,
        order_by: Optional[Sorting] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List AI Prompt Fine-Tuning Jobs

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.jobs.getMany
        """

        params = {
            "statuses": convert_enum_collection_to_string_if_exists(statuses),
            "orderBy": order_by,
            "limit": limit,
            "offset": offset,
        }

        return self.requester.request(
            method="get",
            path=f"users/{user_id}/ai/prompts/fine-tuning/jobs",
            params=params
        )

    def create_ai_prompt_fine_tuning_job(
        self,
        user_id: int,
        ai_prompt_id: int,
        request_data: CreateAIPromptFineTuningJobRequest
    ):
        """
        Create AI Prompt Fine-Tuning Job

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.jobs.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_prompt_fine_tuning_jobs_path(user_id, ai_prompt_id),
            request_data=request_data,
        )

    def get_ai_prompt_fine_tuning_job_status(
        self,
        user_id: int,
        ai_prompt_id: int,
        job_identifier: str
    ):
        """
        Get AI Prompt Fine-Tuning Job Status

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.prompts.fine-tuning.jobs.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_fine_tuning_jobs_path(user_id, ai_prompt_id, job_identifier),
        )

    def download_ai_prompt_fine_tuning_dataset(
        self,
        user_id: int,
        ai_prompt_id: int,
        job_identifier: str
    ):
        """
        Download AI Prompt Fine-Tuning Dataset

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.prompts.fine-tuning.datasets.download.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_fine_tuning_datasets_path(user_id, ai_prompt_id, job_identifier) + "/download",
        )

    def get_ai_custom_placeholders_path(self, user_id: int, custom_placeholder_id: Optional[int] = None):
        if custom_placeholder_id is not None:
            return f"users/{user_id}/ai/settings/custom-placeholders/{custom_placeholder_id}"

        return f"users/{user_id}/ai/settings/custom-placeholders"

    def list_ai_custom_placeholders(self, user_id: int):
        """
        List AI Custom Placeholders

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.ai.prompt.custom.placeholders.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_custom_placeholders_path(user_id)
        )

    def add_ai_custom_placeholder(self, user_id: int, body: AddAiCustomPlaceholderRequest):
        """
        Add AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.settings.custom-placeholders.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_custom_placeholders_path(user_id),
            request_data=body,
        )

    def get_ai_custom_placeholder(self, user_id: int, ai_custom_placeholder_id: int):
        """
        Get AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.settings.custom-placeholders.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_custom_placeholders_path(user_id, ai_custom_placeholder_id),
        )

    def delete_ai_custom_placeholder(self, user_id: int, ai_custom_placeholder_id: int):
        """
        Delete AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.settings.custom-placeholders.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_ai_custom_placeholders_path(user_id, ai_custom_placeholder_id),
        )

    def edit_ai_custom_placeholder(
        self,
        user_id: int,
        ai_custom_placeholder_id: int,
        patches: Iterable[EditAiCustomPlaceholderPatch]
    ):
        """
        Edit AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.settings.custom-placeholders.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_ai_custom_placeholders_path(user_id, ai_custom_placeholder_id),
            request_data=patches,
        )

    def clone_ai_prompt(
        self,
        user_id: int,
        ai_prompt_id: int,
        name: Optional[str] = None,
    ):
        """
        Clone AI Prompt

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.prompts.clones.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_path(user_id, ai_prompt_id) + "/clones",
            request_data={
                "name": name
            },
        )

    def get_ai_prompt_completions_path(
        self,
        user_id: int,
        ai_prompt_id: int,
        completion_id: Optional[str] = None,
    ):
        if completion_id is not None:
            return f"users/{user_id}/ai/prompts/{ai_prompt_id}/completions/{completion_id}"
        return f"users/{user_id}/ai/prompts/{ai_prompt_id}/completions"

    def generate_ai_prompt_completion(
        self,
        user_id: int,
        ai_prompt_id: int,
        request: GenerateAiPromptCompletionRequest
    ):
        """
        Generate AI Prompt Completion

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.ai.prompts.completions.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_prompt_completions_path(user_id, ai_prompt_id),
            request_data=request,
        )

    def get_ai_prompt_completion_status(
        self,
        user_id: int,
        ai_prompt_id: int,
        completion_id: str
    ):
        """
        Get AI Prompt Completion Status

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.prompts.completions.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_completions_path(user_id, ai_prompt_id, completion_id),
        )

    def cancel_ai_prompt_completion(
        self,
        user_id: int,
        ai_prompt_id: int,
        completion_id: str
    ):
        """
        Cancel AI Prompt Completion

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.prompts.completions.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_ai_prompt_completions_path(user_id, ai_prompt_id, completion_id),
        )

    def download_ai_prompt_completion(
        self,
        user_id: int,
        ai_prompt_id: int,
        completion_id: str
    ):
        """
        Download AI Prompt Completion

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.prompts.completions.download.download
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_completions_path(user_id, ai_prompt_id, completion_id) + "/download",
        )

    def get_ai_reports_path(self, user_id: int, ai_report_id: Optional[str] = None):
        if ai_report_id is not None:
            return f"users/{user_id}/ai/reports/{ai_report_id}"
        return f"users/{user_id}/ai/reports"

    def generate_ai_report(
        self,
        user_id: int,
        request: GenerateAiReportRequest
    ):
        """
        Generate AI Report

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.reports.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_reports_path(user_id),
            request_data=request,
        )

    def check_ai_report_generation_status(
        self,
        user_id: int,
        ai_report_id: str,
    ):
        """
        Check AI Report Generation Status

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.reports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_reports_path(user_id, ai_report_id),
        )

    def download_ai_report(
        self,
        user_id: int,
        ai_report_id: str
    ):
        """
        Download AI Report

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.reports.download.download
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_reports_path(user_id, ai_report_id) + "/download",
        )

    def get_ai_settings_path(self, user_id: int):
        return f"users/{user_id}/ai/settings"

    def get_ai_settings(
        self,
        user_id: int,
    ):
        """
        Get AI Settings

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.settings.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_settings_path(user_id),
        )

    def edit_ai_settings(
        self,
        user_id: int,
        patches: Iterable[EditAiSettingsPatch]
    ):
        """
        Edit AI Settings

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/AI/operation/api.users.ai.settings.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_ai_settings_path(user_id),
            request_data=patches,
        )


class EnterpriseAIResource(BaseResource):
    """
    Enterprise Resource for AI.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/AI
    """

    def get_ai_path(self, aiPromptId: Optional[int] = None):
        if aiPromptId is not None:
            return f"ai/prompts/{aiPromptId}"
        return "ai/prompts"

    def get_ai_provider_path(self, aiProviderId: Optional[int] = None):
        if aiProviderId is not None:
            return f"ai/providers/{aiProviderId}"
        return "ai/providers"

    def list_ai_prompts(
        self,
        projectId: Optional[int] = None,
        action: Optional[AIPromptAction] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List AI Prompts

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.prompts.getMany
        """
        params = {"projectId": projectId, "action": action}
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self.requester.request(
            method="get", path=self.get_ai_path(), params=params
        )

    def add_ai_prompt(self, request_data: AddAIPromptRequestScheme):
        """
        Add AI Prompt

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.prompts.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_path(),
            request_data=request_data,
        )

    def get_ai_prompt(self, aiPromptId: int):
        """
        Get AI Prompt

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.prompts.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_path(aiPromptId=aiPromptId),
        )

    def delete_ai_prompt(self, aiPromptId: int):
        """
        Delete AI Prompt

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.prompts.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_ai_path(aiPromptId=aiPromptId),
        )

    def edit_ai_prompt(
        self, aiPromptId: int, request_data: Iterable[EditAIPromptScheme]
    ):
        """
        Edit AI Prompt

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.prompts.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_ai_path(aiPromptId=aiPromptId),
            request_data=request_data,
        )

    def list_ai_providers(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List AI Providers

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.providers.getMany
        """
        params = self.get_page_params(limit=limit, offset=offset)
        return self.requester.request(
            method="get", path=self.get_ai_provider_path(), params=params
        )

    def add_ai_provider(self, request_data: AddAIProviderReqeustScheme):
        """
        Add AI Provider

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.providers.post
        """
        return self.requester.request(
            method="post",
            path=self.get_ai_provider_path(),
            request_data=request_data,
        )

    def get_ai_provider(self, aiProviderId: int):
        """
        Get AI Provider

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.providers.get
        """
        return self.requester.request(
            method="get",
            path=self.get_ai_provider_path(aiProviderId=aiProviderId),
        )

    def delete_ai_provider(self, aiProviderId: int):
        """
        Delete AI Provider

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.providers.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_ai_provider_path(aiProviderId=aiProviderId),
        )

    def edit_ai_provider(
        self, aiProviderId: int, request_data: EditAIProviderRequestScheme
    ):
        """
        Edit AI Provider

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.providers.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_ai_provider_path(aiProviderId=aiProviderId),
            request_data=request_data,
        )

    def list_ai_provider_models(self, aiProviderId: int):
        """
        List AI Provider Models

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.ai.providers.models.getMany
        """
        return self.requester.request(
            method="get",
            path=self.get_ai_provider_path(aiProviderId=aiProviderId) + "/models",
        )

    def create_ai_proxy_chat_completion(
        self,
        aiProviderId: int,
        request_data: Union[GoogleGeminiChatProxy, OtherChatProxy],
    ):
        """
        Create AI Proxy Chat Completion

        This API method serves as an intermediary, forwarding your requests directly to the selected provider.
        Please refer to the documentation for the specific provider you use to determine the required payload format.

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.ai.providers.chat.completions.post
        """
        return self.requester.request(
            method="post",
            path=self.get_ai_provider_path(aiProviderId=aiProviderId)
            + "/chat/completions",
            request_data=request_data,
        )

    def get_ai_custom_placeholders_path(self, ai_custom_placeholder_id: Optional[int] = None):
        if ai_custom_placeholder_id is not None:
            return f"ai/settings/custom-placeholders/{ai_custom_placeholder_id}"
        return "ai/settings/custom-placeholders"

    def list_ai_custom_placeholders(self):
        """
        List AI Custom Placeholders

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.custom.placeholders.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_custom_placeholders_path()
        )

    def add_ai_custom_placeholder(self, body: AddAiCustomPlaceholderRequest):
        """
        Add AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.settings.custom-placeholders.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_custom_placeholders_path(),
            request_data=body,
        )

    def get_ai_custom_placeholder(self, ai_custom_placeholder_id: int):
        """
        Get AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.settings.custom-placeholders.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_custom_placeholders_path(ai_custom_placeholder_id),
        )

    def delete_ai_custom_placeholder(self, ai_custom_placeholder_id: int):
        """
        Delete AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.settings.custom-placeholders.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_ai_custom_placeholders_path(ai_custom_placeholder_id),
        )

    def edit_ai_custom_placeholder(
        self,
        ai_custom_placeholder_id: int,
        patches: Iterable[EditAiCustomPlaceholderPatch]
    ):
        """
        Edit AI Custom Placeholder

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.settings.custom-placeholders.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_ai_custom_placeholders_path(ai_custom_placeholder_id),
            request_data=patches,
        )

    def get_ai_prompt_fine_tuning_datasets_path(
        self,
        ai_prompt_id: int,
        job_identifier: Optional[str] = None
    ):
        if job_identifier is not None:
            return f"ai/prompts/{ai_prompt_id}/fine-tuning/datasets/{job_identifier}"
        return f"ai/prompts/{ai_prompt_id}/fine-tuning/datasets"

    def generate_ai_prompt_fine_tuning_dataset(
        self,
        ai_prompt_id: int,
        request_data: GenerateAIPromptFineTuningDatasetRequest,
    ):
        """
        Generate AI Prompt Fine-Tuning Dataset

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.datasets.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_prompt_fine_tuning_datasets_path(ai_prompt_id),
            request_data=request_data,
        )

    def get_ai_prompt_fine_tuning_dataset_generation_status(
        self,
        ai_prompt_id: int,
        job_identifier: str
    ):
        """
        Get AI Prompt Fine-Tuning Dataset Generation Status

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.datasets.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_fine_tuning_datasets_path(ai_prompt_id, job_identifier),
        )

    def list_ai_prompt_fine_tuning_events(
        self,
        ai_prompt_id: int,
        job_identifier: str,
    ):
        """
        List AI Prompt Fine-Tuning Events

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.jobs.events.getMany
        """

        return self.requester.request(
            method="get",
            path=f"ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}/events",
        )

    def list_ai_prompt_fine_tuning_jobs(
        self,
        statuses: Optional[Iterable[AiPromptFineTuningJobStatus]] = None,
        order_by: Optional[Sorting] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List AI Prompt Fine-Tuning Jobs

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.jobs.getMany
        """

        params = {
            "statuses": convert_enum_collection_to_string_if_exists(statuses),
            "orderBy": order_by,
            "limit": limit,
            "offset": offset,
        }

        return self.requester.request(
            method="get",
            path="ai/prompts/fine-tuning/jobs",
            params=params
        )

    def get_ai_prompt_fine_tuning_jobs_path(
        self,
        ai_prompt_id: int,
        job_identifier: Optional[str] = None
    ):
        if job_identifier is not None:
            return f"ai/prompts/{ai_prompt_id}/fine-tuning/jobs/{job_identifier}"
        return f"ai/prompts/{ai_prompt_id}/fine-tuning/jobs"

    def create_ai_prompt_fine_tuning_job(
        self,
        ai_prompt_id: int,
        request_data: CreateAIPromptFineTuningJobRequest
    ):
        """
        Create AI Prompt Fine-Tuning Job

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.jobs.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_prompt_fine_tuning_jobs_path(ai_prompt_id),
            request_data=request_data,
        )

    def get_ai_prompt_fine_tuning_job_status(
        self,
        ai_prompt_id: int,
        job_identifier: str
    ):
        """
        Get AI Prompt Fine-Tuning Job Status

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.jobs.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_fine_tuning_jobs_path(ai_prompt_id, job_identifier),
        )

    def download_ai_prompt_fine_tuning_dataset(
        self,
        ai_prompt_id: int,
        job_identifier: str
    ):
        """
        Download AI Prompt Fine-Tuning Dataset

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.fine-tuning.datasets.download.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_fine_tuning_datasets_path(ai_prompt_id, job_identifier) + "/download",
        )

    def clone_ai_prompt(
        self,
        ai_prompt_id: int,
        name: Optional[str] = None,
    ):
        """
        Clone AI Prompt

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.clones.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_path(ai_prompt_id) + "/clones",
            request_data={
                "name": name
            },
        )

    def get_ai_prompt_completions_path(
        self,
        ai_prompt_id: int,
        completion_id: Optional[str] = None
    ):
        if completion_id is not None:
            return f"ai/prompts/{ai_prompt_id}/completions/{completion_id}"
        return f"ai/prompts/{ai_prompt_id}/completions"

    def generate_ai_prompt_completion(
        self,
        ai_prompt_id: int,
        request: GenerateAiPromptCompletionRequest
    ):
        """
        Generate AI Prompt Completion

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.completions.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_prompt_completions_path(ai_prompt_id),
            request_data=request,
        )

    def get_ai_prompt_completion_status(
        self,
        ai_prompt_id: int,
        completion_id: str
    ):
        """
        Get AI Prompt Completion Status

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.completions.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_completions_path(ai_prompt_id, completion_id),
        )

    def cancel_ai_prompt_completion(
        self,
        ai_prompt_id: int,
        completion_id: str
    ):
        """
        Cancel AI Prompt Completion

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.completions.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_ai_prompt_completions_path(ai_prompt_id, completion_id),
        )

    def download_ai_prompt_completion(
        self,
        ai_prompt_id: int,
        completion_id: str
    ):
        """
        Download AI Prompt Completion

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.prompts.completions.download.download
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_prompt_completions_path(ai_prompt_id, completion_id) + "/download",
        )

    def get_ai_reports_path(self, ai_report_id: Optional[str] = None):
        if ai_report_id is not None:
            return f"ai/reports/{ai_report_id}"
        return "ai/reports"

    def generate_ai_report(
        self,
        request: GenerateAiReportRequest
    ):
        """
        Generate AI Report

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.reports.post
        """

        return self.requester.request(
            method="post",
            path=self.get_ai_reports_path(),
            request_data=request,
        )

    def check_ai_report_generation_status(
        self,
        ai_report_id: str,
    ):
        """
        Check AI Report Generation Status

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.reports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_reports_path(ai_report_id),
        )

    def download_ai_report(
        self,
        ai_report_id: str
    ):
        """
        Download AI Report

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.reports.download.download
        """

        return self.requester.request(
            method="get",
            path=self.get_ai_reports_path(ai_report_id) + "/download",
        )

    def get_ai_settings(self):
        """
        Get AI Settings

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.settings.get
        """

        return self.requester.request(
            method="get",
            path="ai/settings",
        )

    def edit_ai_settings(
        self,
        patches: Iterable[EditAiSettingsPatch]
    ):
        """
        Edit AI Settings

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/AI/operation/api.ai.settings.patch
        """

        return self.requester.request(
            method="patch",
            path="ai/settings",
            request_data=patches,
        )
