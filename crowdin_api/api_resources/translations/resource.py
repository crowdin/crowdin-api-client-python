from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import ExportProjectTranslationFormat
from crowdin_api.api_resources.translations.types import (
    FallbackLanguages,
    EditPreTranslationScheme,
    UploadTranslationRequest,
)
from crowdin_api.api_resources.translations.enums import (
    CharTransformation,
    PreTranslationApplyMethod,
    PreTranslationAutoApproveOption,
)


class TranslationsResource(BaseResource):
    """
    Resource for Translations.

    Translators can work with entirely untranslated project or you can pre-translate the files to
    ease the translations process.

    Use API to pre-translate files via Machine Translation (MT) or Translation Memory (TM), upload
    your existing translations, and download translations correspondingly. Pre-translate and build
    are asynchronous operations and shall be completed with sequence of API methods.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Translations
    """

    def get_builds_path(self, projectId: int, buildId: Optional[int] = None):
        if buildId:
            return f"projects/{projectId}/translations/builds/{buildId}"

        return f"projects/{projectId}/translations/builds"

    def pre_translation_status(
        self, preTranslationId: str, projectId: Optional[int] = None
    ):
        """
        Pre-Translation Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#tag/Translations/paths/~1projects~1{projectId}~1pre-translations~1{preTranslationId}/get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=f"projects/{projectId}/pre-translations/{preTranslationId}",
        )

    def list_pre_translations(
        self,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Pre-Translations

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.pre-translations.getMany
        """
        projectId = projectId or self.get_project_id()

        params = self.get_page_params(page=page, offset=offset, limit=limit)

        return self.requester.request(
            method="get",
            path=f"projects/{projectId}/pre-translations",
            params=params,
        )

    def apply_pre_translation(
        self,
        languageIds: Iterable[str],
        fileIds: Iterable[int],
        projectId: Optional[int] = None,
        method: Optional[PreTranslationApplyMethod] = None,
        engineId: Optional[int] = None,
        aiPromptId: Optional[int] = None,
        autoApproveOption: Optional[PreTranslationAutoApproveOption] = None,
        duplicateTranslations: Optional[bool] = None,
        skipApprovedTranslations: Optional[bool] = None,
        translateUntranslatedOnly: Optional[bool] = None,
        translateWithPerfectMatchOnly: Optional[bool] = None,
        fallbackLanguages: Optional[Iterable[FallbackLanguages]] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
    ):
        """
        Apply Pre-Translation.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.pre-translations.post
        """
        if fallbackLanguages is None:
            fallbackLanguages = []

        if labelIds is None:
            labelIds = []

        if excludeLabelIds is None:
            excludeLabelIds = []

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/pre-translations",
            request_data={
                "languageIds": languageIds,
                "fileIds": fileIds,
                "method": method,
                "engineId": engineId,
                "aiPromptId": aiPromptId,
                "autoApproveOption": autoApproveOption,
                "duplicateTranslations": duplicateTranslations,
                "skipApprovedTranslations": skipApprovedTranslations,
                "translateUntranslatedOnly": translateUntranslatedOnly,
                "translateWithPerfectMatchOnly": translateWithPerfectMatchOnly,
                "fallbackLanguages": fallbackLanguages,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
            },
        )

    def edit_pre_translation(
        self,
        preTranslationId: str,
        data: Iterable[EditPreTranslationScheme],
        projectId: Optional[int] = None,
    ):
        """
        Edit Pre-Translation

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.pre-translations.patch
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=f"projects/{projectId}/pre-translations/{preTranslationId}",
            request_data=data,
        )

    def build_project_directory_translation(
        self,
        directoryId: int,
        projectId: Optional[int] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
    ):
        """
        Build Project Directory Translation.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.directories.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"{self.get_builds_path(projectId=projectId)}/directories/{directoryId}",
            request_data={
                "targetLanguageIds": targetLanguageIds,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "skipUntranslatedFiles": skipUntranslatedFiles,
                "exportApprovedOnly": exportApprovedOnly,
            },
        )

    def build_project_file_translation(
        self,
        fileId: int,
        targetLanguageId: str,
        projectId: Optional[int] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
        eTag: Optional[str] = None,
    ):
        """
        Build Project File Translation.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.files.post
        """

        if eTag is not None:
            headers = {"If-None-Match": eTag}
        else:
            headers = None

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            headers=headers,
            path=f"{self.get_builds_path(projectId=projectId)}/files/{fileId}",
            request_data={
                "targetLanguageId": targetLanguageId,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "skipUntranslatedFiles": skipUntranslatedFiles,
                "exportApprovedOnly": exportApprovedOnly,
            },
        )

    def list_project_builds(
        self,
        projectId: Optional[int] = None,
        branchId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Project Builds.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"branchId": branchId}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_builds_path(projectId=projectId),
            params=params,
        )

    def build_project_translation(
        self, request_data: Dict, projectId: Optional[int] = None
    ):
        """
        Build Project Translation.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_builds_path(projectId=projectId),
            request_data=request_data,
        )

    def build_crowdin_project_translation(
        self,
        projectId: Optional[int] = None,
        branchId: Optional[int] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
        exportWithMinApprovalsCount: Optional[int] = None,
    ):
        """
        Build Project Translation(Crowdin Translation Create Project Build Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.post
        """

        projectId = projectId or self.get_project_id()

        return self.build_project_translation(
            projectId=projectId,
            request_data={
                "branchId": branchId,
                "targetLanguageIds": targetLanguageIds,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "skipUntranslatedFiles": skipUntranslatedFiles,
                "exportApprovedOnly": exportApprovedOnly,
                "exportWithMinApprovalsCount": exportWithMinApprovalsCount,
            },
        )

    def build_pseudo_project_translation(
        self,
        pseudo: bool,
        projectId: Optional[int] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        lengthTransformation: Optional[int] = None,
        charTransformation: Optional[CharTransformation] = None,
    ):
        """
        Build Project Translation(Translation Create Project Pseudo Build Form).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.post
        """

        projectId = projectId or self.get_project_id()

        return self.build_project_translation(
            projectId=projectId,
            request_data={
                "pseudo": pseudo,
                "prefix": prefix,
                "suffix": suffix,
                "lengthTransformation": lengthTransformation,
                "charTransformation": charTransformation,
            },
        )

    def upload_translation(
        self,
        languageId: str,
        storageId: int,
        fileId: int,
        projectId: Optional[int] = None,
        importEqSuggestions: Optional[bool] = None,
        autoApproveImported: Optional[bool] = None,
        translateHidden: Optional[bool] = None,
        addToTm: Optional[bool] = None,
    ):
        """
        Upload Translations.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.postOnLanguage
        """
        projectId = projectId or self.get_project_id()

        request_data: UploadTranslationRequest = {
            "storageId": storageId,
            "fileId": fileId,
            "importEqSuggestions": importEqSuggestions,
            "autoApproveImported": autoApproveImported,
            "translateHidden": translateHidden,
            "addToTm": addToTm,
        }

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/translations/{languageId}",
            request_data=request_data,
        )

    def download_project_translations(
        self, buildId: int, projectId: Optional[int] = None
    ):
        """
        Download Project Translations.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.download.download
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=f"{self.get_builds_path(projectId=projectId, buildId=buildId)}/download",
        )

    def check_project_build_status(self, buildId: int, projectId: Optional[int] = None):
        """
        Check Project Build Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_builds_path(projectId=projectId, buildId=buildId),
        )

    def cancel_build(self, buildId: int, projectId: Optional[int] = None):
        """
        Cancel Build.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.builds.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_builds_path(projectId=projectId, buildId=buildId),
        )

    def export_project_translation(
        self,
        targetLanguageId: str,
        projectId: Optional[int] = None,
        format: Optional[ExportProjectTranslationFormat] = None,
        labelIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
        directoryIds: Optional[Iterable[int]] = None,
        fileIds: Optional[Iterable[int]] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
    ):
        """
        Export Project Translation.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.translations.exports.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/translations/exports",
            request_data={
                "targetLanguageId": targetLanguageId,
                "format": format,
                "labelIds": labelIds,
                "branchIds": branchIds,
                "directoryIds": directoryIds,
                "fileIds": fileIds,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "skipUntranslatedFiles": skipUntranslatedFiles,
                "exportApprovedOnly": exportApprovedOnly,
            },
        )
