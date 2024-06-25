from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.ai.enums import AIPromptAction
from crowdin_api.api_resources.ai.types import AddAIPromptRequestScheme, EditAIPromptScheme


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
