from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import ExportProjectTranslationFormat
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
    https://support.crowdin.com/api/v2/#tag/Translations
    """

    def get_builds_path(self, projectId: int, buildId: Optional[str] = None):
        if buildId:
            return f"projects/{projectId}/translations/builds/{buildId}"

        return f"projects/{projectId}/translations/builds"

    def pre_translation_status(self, projectId: int, preTranslationId: str):
        """
        Pre-Translation Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#tag/Translations/paths/~1projects~1{projectId}~1pre-translations~1{preTranslationId}/get
        """

        return self.requester.request(
            method="get",
            path=f"projects/{projectId}/pre-translations/{preTranslationId}",
        )

    def apply_pre_translation(
        self,
        projectId: int,
        languageIds: Iterable[str],
        fileIds: Iterable[int],
        method: Optional[PreTranslationApplyMethod] = None,
        engineId: Optional[int] = None,
        autoApproveOption: Optional[PreTranslationAutoApproveOption] = None,
        duplicateTranslations: Optional[bool] = None,
        translateUntranslatedOnly: Optional[bool] = None,
        translateWithPerfectMatchOnly: Optional[bool] = None,
    ):
        """
        Apply Pre-Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.pre-translations.post
        """

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/pre-translations",
            request_data={
                "languageIds": languageIds,
                "fileIds": fileIds,
                "method": method,
                "engineId": engineId,
                "autoApproveOption": autoApproveOption,
                "duplicateTranslations": duplicateTranslations,
                "translateUntranslatedOnly": translateUntranslatedOnly,
                "translateWithPerfectMatchOnly": translateWithPerfectMatchOnly,
            },
        )

    def build_project_file_translation(
        self,
        projectId: int,
        fileId: int,
        targetLanguageId: str,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
        eTag: Optional[str] = None,
    ):
        """
        Build Project File Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.files.post
        """

        if eTag is not None:
            headers = {"If-None-Match": eTag}
        else:
            headers = None

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
        projectId: int,
        branchId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Project Builds.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.getMany
        """

        params = {"branchId": branchId}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_builds_path(projectId=projectId),
            params=params,
        )

    def build_project_translation(self, projectId: int, request_data: Dict):
        """
        Build Project Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.post
        """

        return self.requester.request(
            method="post",
            path=self.get_builds_path(projectId=projectId),
            request_data=request_data,
        )

    def build_crowdin_project_translation(
        self,
        projectId: int,
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
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.post
        """

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
        projectId: int,
        pseudo: bool,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        lengthTransformation: Optional[int] = None,
        charTransformation: Optional[CharTransformation] = None,
    ):
        """
        Build Project Translation(Translation Create Project Pseudo Build Form).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.post
        """

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
        projectId: int,
        languageId: str,
        storageId: int,
        fileId: int,
        importEqSuggestions: Optional[bool] = None,
        autoApproveImported: Optional[bool] = None,
        translateHidden: Optional[bool] = None,
    ):
        """
        Upload Translations.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.postOnLanguage
        """

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/translations/{languageId}",
            request_data={
                "storageId": storageId,
                "fileId": fileId,
                "importEqSuggestions": importEqSuggestions,
                "autoApproveImported": autoApproveImported,
                "translateHidden": translateHidden,
            },
        )

    def download_project_translations(self, projectId: int, buildId: str):
        """
        Download Project Translations.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.download.download
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_builds_path(projectId=projectId, buildId=buildId)}/download",
        )

    def check_project_build_status(self, projectId: int, buildId: str):
        """
        Check Project Build Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.get
        """

        return self.requester.request(
            method="get",
            path=self.get_builds_path(projectId=projectId, buildId=buildId),
        )

    def cancel_build(self, projectId: int, buildId: str):
        """
        Cancel Build.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_builds_path(projectId=projectId, buildId=buildId),
        )

    def export_project_translation(
        self,
        projectId: int,
        targetLanguageId: str,
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
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.exports.post
        """

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
