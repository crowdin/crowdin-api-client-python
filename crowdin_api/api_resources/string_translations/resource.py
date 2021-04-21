from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import DenormalizePlaceholders, PluralCategoryName
from crowdin_api.api_resources.string_translations.enums import VoteMark


class StringTranslationsResource(BaseResource):
    """
    Resource for String Translations.

    Use API to add or remove strings translations, approvals, and votes.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/String-Translations
    """

    # Approval
    def get_approvals_path(self, projectId: int, approvalId: Optional[int] = None):
        if approvalId is not None:
            return f"projects/{projectId}/approvals/{approvalId}"

        return f"projects/{projectId}/approvals"

    def list_translation_approvals(
        self,
        projectId: int,
        fileId: Optional[int] = None,
        stringId: Optional[int] = None,
        languageId: Optional[str] = None,
        translationId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Translation Approvals

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.approvals.getMany
        """

        params = {
            "fileId": fileId,
            "stringId": stringId,
            "languageId": languageId,
            "translationId": translationId,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_approvals_path(projectId=projectId),
            params=params,
        )

    def add_approval(
        self,
        projectId: int,
        translationId: int,
    ):
        """
        Add Approval.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.approvals.post
        """

        return self.requester.request(
            method="post",
            path=self.get_approvals_path(projectId=projectId),
            request_data={"translationId": translationId},
        )

    def get_approval(self, projectId: int, approvalId: int):
        """
        Get Approval.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.approvals.get
        """

        return self.requester.request(
            method="get",
            path=self.get_approvals_path(projectId=projectId, approvalId=approvalId),
        )

    def remove_approval(self, projectId: int, approvalId: int):
        """
        Remove Approvall.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.approvals.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_approvals_path(projectId=projectId, approvalId=approvalId),
        )

    # Language Translations
    def list_language_translations(
        self,
        projectId: int,
        languageId: str,
        stringIds: Optional[Iterable[int]] = None,
        labelIds: Optional[Iterable[int]] = None,
        fileId: Optional[int] = None,
        croql: Optional[str] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Language Translations

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.languages.translations.getMany
        """

        params = {
            "stringIds": None
            if stringIds is None
            else ",".join(str(stringId) for stringId in stringIds),
            "labelIds": None
            if labelIds is None
            else ",".join(str(labelId) for labelId in labelIds),
            "fileId": fileId,
            "croql": croql,
            "denormalizePlaceholders": denormalizePlaceholders,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=f"projects/{projectId}/languages/{languageId}/translations",
            params=params,
        )

    # Translations
    def get_translations_path(self, projectId: int, translationId: Optional[int] = None):
        if translationId is not None:
            return f"projects/{projectId}/translations/{translationId}"

        return f"projects/{projectId}/translations"

    def list_string_translations(
        self,
        projectId: int,
        stringId: Optional[int] = None,
        languageId: Optional[str] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List String Translations

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.getMany
        """

        params = {
            "stringId": stringId,
            "languageId": languageId,
            "denormalizePlaceholders": denormalizePlaceholders,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_translations_path(projectId=projectId),
            params=params,
        )

    def add_translation(
        self,
        projectId: int,
        stringId: int,
        languageId: str,
        text: str,
        pluralCategoryName: Optional[PluralCategoryName] = None,
    ):
        """
        Add Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.post
        """

        return self.requester.request(
            method="post",
            path=self.get_translations_path(projectId=projectId),
            request_data={
                "stringId": stringId,
                "languageId": languageId,
                "text": text,
                "pluralCategoryName": pluralCategoryName,
            },
        )

    def delete_string_translations(self, projectId: int, stringId: int, languageId: str):
        """
        Delete String Translations.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.deleteMany
        """

        return self.requester.request(
            method="delete",
            params={"stringId": stringId, "languageId": languageId},
            path=self.get_translations_path(projectId=projectId),
        )

    def get_translation(self, projectId: int, translationId: int):
        """
        Get Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.get
        """

        return self.requester.request(
            method="get",
            path=self.get_translations_path(projectId=projectId, translationId=translationId),
        )

    def restore_translation(self, projectId: int, translationId: int):
        """
        Restore Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.put
        """

        return self.requester.request(
            method="put",
            path=self.get_translations_path(projectId=projectId, translationId=translationId),
        )

    def delete_translation(self, projectId: int, translationId: int):
        """
        Delete Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_translations_path(projectId=projectId, translationId=translationId),
        )

    # Translation Votes
    def get_translation_votes_path(self, projectId: int, voteId: Optional[int] = None):
        if voteId is not None:
            return f"projects/{projectId}/votes/{voteId}"

        return f"projects/{projectId}/votes"

    def list_translation_votes(
        self,
        projectId: int,
        stringId: Optional[int] = None,
        languageId: Optional[str] = None,
        translationId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Translation Votes

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.votes.getMany
        """

        params = {
            "stringId": stringId,
            "languageId": languageId,
            "translationId": translationId,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_translation_votes_path(projectId=projectId),
            params=params,
        )

    def add_vote(self, projectId: int, mark: VoteMark, translationId: int):
        """
        Add Vote.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.votes.pos
        """

        return self.requester.request(
            method="post",
            path=self.get_translation_votes_path(projectId=projectId),
            request_data={"translationId": translationId, "mark": mark},
        )

    def get_vote(self, projectId: int, voteId: int):
        """
        Get Vote.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.votes.get
        """

        return self.requester.request(
            method="get",
            path=self.get_translation_votes_path(projectId=projectId, voteId=voteId),
        )

    def cancel_vote(self, projectId: int, voteId: int):
        """
        Cancel Vote.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.votes.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_translation_votes_path(projectId=projectId, voteId=voteId),
        )
