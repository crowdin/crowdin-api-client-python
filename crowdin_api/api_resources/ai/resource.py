from typing import Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.ai.enums import AIPromptAction
from crowdin_api.api_resources.ai.types import (
    AddAIPromptRequestScheme,
    AddAIProviderReqeustScheme,
    EditAIPromptScheme,
    EditAIProviderRequestScheme,
    GoogleGeminiChatProxy,
    OtherChatProxy,
)


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
