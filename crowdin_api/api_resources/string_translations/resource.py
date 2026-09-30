from typing import Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import DenormalizePlaceholders, PluralCategoryName
from crowdin_api.api_resources.string_translations.enums import TranslationProvider, VoteMark
from crowdin_api.api_resources.string_translations.types import (
    ApprovalBatchOpPatchRequest,
    TranslationBatchOpPatchRequest
)
from crowdin_api.sorting import Sorting


class StringTranslationsResource(BaseResource):
    """
    Resource for String Translations.

    Use API to add or remove strings translations, approvals, and votes.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/String-Translations
    """

    def search_translations(
        self,
        filter: str,
        projectIds: Optional[Iterable[int]] = None,
        userId: Optional[int] = None,
        languageIds: Optional[Iterable[str]] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Search Translations.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.translations.getMany
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.translations.getMany
        """

        params = {
            "filter": filter,
            "projectIds": None
            if projectIds is None
            else ",".join(str(projectId) for projectId in projectIds),
            "userId": userId,
            "languageIds": None
            if languageIds is None
            else ",".join(str(languageId) for languageId in languageIds),
            "denormalizePlaceholders": denormalizePlaceholders,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(method="get", path="translations", params=params)

    # Approval
    def get_approvals_path(self, projectId: int, approvalId: Optional[int] = None):
        if approvalId is not None:
            return f"projects/{projectId}/approvals/{approvalId}"

        return f"projects/{projectId}/approvals"

    def list_translation_approvals(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        fileId: Optional[int] = None,
        labelIds: Optional[str] = None,
        excludeLabelIds: Optional[str] = None,
        stringId: Optional[int] = None,
        languageId: Optional[str] = None,
        translationId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        correctionId: Optional[int] = None,
    ):
        """
        List Translation Approvals

        `fileId` is available in file-based projects only, `correctionId` in Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.approvals.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.approvals.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "fileId": fileId,
            "labelIds": labelIds,
            "excludeLabelIds": excludeLabelIds,
            "stringId": stringId,
            "languageId": languageId,
            "translationId": translationId,
            "correctionId": correctionId,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_approvals_path(projectId=projectId),
            params=params,
        )

    def add_approval(
        self,
        translationId: Optional[int] = None,
        projectId: Optional[int] = None,
        correctionId: Optional[int] = None,
    ):
        """
        Add Approval.

        Pass either `translationId` or `correctionId` (Crowdin Enterprise only).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.approvals.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.approvals.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_approvals_path(projectId=projectId),
            request_data={"translationId": translationId, "correctionId": correctionId},
        )

    def remove_string_approvals(
        self,
        stringId: Optional[int] = None,
        projectId: Optional[int] = None,
        fileId: Optional[int] = None,
    ):
        """
        Remove String Approvals

        Remove approvals of a string (`stringId`) or of all strings in a file
        (`fileId`, file-based projects only). `stringId` is required in string-based projects.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/String-Translations/operation/api.projects.approvals.deleteMany
        """

        projectId = projectId or self.get_project_id()

        params = {"stringId": stringId, "fileId": fileId}

        return self.requester.request(
            method="delete", path=self.get_approvals_path(projectId=projectId), params=params
        )

    def get_approval(self, approvalId: int, projectId: Optional[int] = None):
        """
        Get Approval.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.approvals.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_approvals_path(projectId=projectId, approvalId=approvalId),
        )

    def remove_approval(self, approvalId: int, projectId: Optional[int] = None):
        """
        Remove Approval.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.approvals.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_approvals_path(projectId=projectId, approvalId=approvalId),
        )

    # Language Translations
    def list_language_translations(
        self,
        languageId: str,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        stringIds: Optional[Iterable[int]] = None,
        labelIds: Optional[Iterable[int]] = None,
        fileId: Optional[int] = None,
        branchId: Optional[int] = None,
        directoryId: Optional[int] = None,
        croql: Optional[str] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        approvedOnly: Optional[Union[bool, int]] = None,
        passedWorkflow: Optional[Union[bool, int]] = None,
        minApprovalCount: Optional[int] = None,
    ):
        """
        List Language Translations

        `fileId` and `directoryId` are available in file-based projects only.
        `orderBy` and `approvedOnly` are available in Crowdin only;
        `passedWorkflow` and `minApprovalCount` in Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.languages.translations.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.languages.translations.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "stringIds": None
            if stringIds is None
            else ",".join(str(stringId) for stringId in stringIds),
            "labelIds": None
            if labelIds is None
            else ",".join(str(labelId) for labelId in labelIds),
            "fileId": fileId,
            "branchId": branchId,
            "directoryId": directoryId,
            "croql": croql,
            "denormalizePlaceholders": denormalizePlaceholders,
            "approvedOnly": None if approvedOnly is None else int(approvedOnly),
            "passedWorkflow": None if passedWorkflow is None else int(passedWorkflow),
            "minApprovalCount": minApprovalCount,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/languages/{languageId}/translations",
            params=params,
        )

    def translation_alignment(
        self,
        sourceLanguageId: str,
        targetLanguageId: str,
        text: str,
        projectId: Optional[int] = None,
    ):
        """
        Translation Alignment

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.alignment.post
        """

        projectId = projectId or self.get_project_id()
        data = {
            "sourceLanguageId": sourceLanguageId,
            "targetLanguageId": targetLanguageId,
            "text": text,
        }

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/translations/alignment",
            request_data=data,
        )

    # Translations
    def get_translations_path(self, projectId: int, translationId: Optional[int] = None):
        if translationId is not None:
            return f"projects/{projectId}/translations/{translationId}"

        return f"projects/{projectId}/translations"

    def list_string_translations(
        self,
        projectId: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
        stringId: Optional[int] = None,
        languageId: Optional[str] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fileId: Optional[int] = None,
    ):
        """
        List String Translations

        `languageId` is required by the API. `fileId` is available in file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "orderBy": orderBy,
            "stringId": stringId,
            "languageId": languageId,
            "denormalizePlaceholders": denormalizePlaceholders,
            "fileId": fileId,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_translations_path(projectId=projectId),
            params=params,
        )

    def add_translation(
        self,
        stringId: int,
        languageId: str,
        text: str,
        projectId: Optional[int] = None,
        pluralCategoryName: Optional[PluralCategoryName] = None,
        addToTm: Optional[bool] = None,
        provider: Optional[TranslationProvider] = None,
        providerId: Optional[int] = None,
        isPreTranslated: Optional[bool] = None,
    ):
        """
        Add Translation.

        `provider` is required when `providerId` or `isPreTranslated` is specified.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.post
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_translations_path(projectId=projectId),
            request_data={
                "stringId": stringId,
                "languageId": languageId,
                "text": text,
                "pluralCategoryName": pluralCategoryName,
                "addToTm": addToTm,
                "provider": provider,
                "providerId": providerId,
                "isPreTranslated": isPreTranslated,
            },
        )

    def add_file_translations(
        self,
        fileId: int,
        languageId: str,
        storageId: int,
        projectId: Optional[int] = None,
    ):
        """
        Add Translation (upload translations of a file from storage).

        File-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.translations.post
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_translations_path(projectId=projectId),
            request_data={
                "fileId": fileId,
                "languageId": languageId,
                "storageId": storageId,
            },
        )

    def delete_string_translations(
        self,
        stringId: Optional[int] = None,
        languageId: Optional[str] = None,
        projectId: Optional[int] = None,
        fileId: Optional[int] = None,
    ):
        """
        Delete String Translations.

        Delete translations of a string (`stringId`) or of all strings in a file
        (`fileId`, file-based projects only). `stringId` is required in string-based projects.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.deleteMany
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            params={"stringId": stringId, "languageId": languageId, "fileId": fileId},
            path=self.get_translations_path(projectId=projectId),
        )

    def get_translation(
        self,
        translationId: int,
        projectId: Optional[int] = None,
        denormalizePlaceholders: Optional[DenormalizePlaceholders] = None,
    ):
        """
        Get Translation.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_translations_path(projectId=projectId, translationId=translationId),
            params={"denormalizePlaceholders": denormalizePlaceholders},
        )

    def restore_translation(self, translationId: int, projectId: Optional[int] = None):
        """
        Restore Translation.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.put
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=self.get_translations_path(projectId=projectId, translationId=translationId),
        )

    def delete_translation(self, translationId: int, projectId: Optional[int] = None):
        """
        Delete Translation.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.delete
        """

        projectId = projectId or self.get_project_id()

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
        projectId: Optional[int] = None,
        stringId: Optional[int] = None,
        languageId: Optional[str] = None,
        translationId: Optional[int] = None,
        fileId: Optional[int] = None,
        labelIds: Optional[str] = None,
        excludeLabelIds: Optional[str] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Translation Votes

        `fileId` is available in file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.votes.getMany
        """

        projectId = projectId or self.get_project_id()

        params = {
            "stringId": stringId,
            "languageId": languageId,
            "translationId": translationId,
            "fileId": fileId,
            "labelIds": labelIds,
            "excludeLabelIds": excludeLabelIds,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_translation_votes_path(projectId=projectId),
            params=params,
        )

    def add_vote(
        self, mark: VoteMark, translationId: int, projectId: Optional[int] = None
    ):
        """
        Add Vote.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.votes.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_translation_votes_path(projectId=projectId),
            request_data={"translationId": translationId, "mark": mark},
        )

    def get_vote(self, voteId: int, projectId: Optional[int] = None):
        """
        Get Vote.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.votes.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_translation_votes_path(projectId=projectId, voteId=voteId),
        )

    def cancel_vote(self, voteId: int, projectId: Optional[int] = None):
        """
        Cancel Vote.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.votes.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_translation_votes_path(projectId=projectId, voteId=voteId),
        )

    def approval_batch_operations(
        self,
        project_id: int,
        data: Iterable[ApprovalBatchOpPatchRequest]
    ):
        """
        Approval Batch Operations

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/String-Translations/operation/api.projects.approvals.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Translations/operation/api.projects.approvals.patch
        """

        return self.requester.request(
            method="patch",
            path=f"projects/{project_id}/approvals",
            request_data=data,
        )

    def translation_batch_operations(
        self,
        project_id: int,
        data: Iterable[TranslationBatchOpPatchRequest]
    ):
        """
        Translation Batch Operations

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/String-Translations/operation/api.projects.translations.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/String-Translations/operation/api.projects.translations.patch
        """

        return self.requester.request(
            method="patch",
            path=f"projects/{project_id}/translations",
            request_data=data,
        )
