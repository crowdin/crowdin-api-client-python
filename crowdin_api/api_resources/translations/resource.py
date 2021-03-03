from typing import List, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.translations.enums import (
    ExportProjectTranslationFormat,
    PreTranslationApplyMethod,
    PreTranslationAutoApproveOption,
)
from crowdin_api.api_resources.translations.types import (
    BuildRequest,
    PseudoBuildRequest,
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

    base_path = "projects"

    def pre_translation_status(self, projectId: int, preTranslationId: str):
        """
        Pre-Translation Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#tag/Translations/paths/~1projects~1{projectId}~1pre-translations~1{preTranslationId}/get
        """

        return self.requester.request(
            method="get",
            path=f"{self.prepare_path(projectId) }/pre-translations/{preTranslationId}",
        )

    def apply_pre_translation(
        self,
        projectId: int,
        languageIds: List[str],
        fileIds: List[int],
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
            path=f"{self.prepare_path(projectId) }/pre-translations",
            post_data={
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
            path=f"{self.prepare_path(object_id=projectId)}/translations/builds/files/{fileId}",
            post_data={
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
            path=f"{self.prepare_path(object_id=projectId)}/translations/builds",
            params=params,
        )

    def build_project_translation(
        self, projectId: int, request_data: Union[PseudoBuildRequest, BuildRequest]
    ):
        """
        Build Project Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.post
        """

        return self.requester.request(
            method="post",
            path=f"{self.prepare_path(object_id=projectId)}/translations/builds/",
            post_data=request_data,
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
            path=f"{self.prepare_path(object_id=projectId)}/translations/{languageId}",
            post_data={
                "storageId": storageId,
                "fileId": fileId,
                "importEqSuggestions": importEqSuggestions,
                "autoApproveImported": autoApproveImported,
                "translateHidden": translateHidden,
            },
        )

    def download_project_translations(
        self,
        projectId: int,
        buildId: str,
    ):
        """
        Download Project Translations.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.download.download
        """

        return self.requester.request(
            method="get",
            path=f"{self.prepare_path(object_id=projectId)}/translations/builds/{buildId}/download",
        )

    def check_project_build_status(
        self,
        projectId: int,
        buildId: str,
    ):
        """
        Check Project Build Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.get
        """

        return self.requester.request(
            method="get",
            path=f"{self.prepare_path(object_id=projectId)}/translations/builds/{buildId}",
        )

    def cancel_build(
        self,
        projectId: int,
        buildId: str,
    ):
        """
        Cancel Build.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.builds.delete
        """

        return self.requester.request(
            method="delete",
            path=f"{self.prepare_path(object_id=projectId)}/translations/builds/{buildId}",
        )

    def export_project_translation(
        self,
        projectId: int,
        targetLanguageId: str,
        format: Optional[ExportProjectTranslationFormat] = None,
        labelIds: Optional[List[int]] = None,
        branchIds: Optional[List[int]] = None,
        directoryIds: Optional[List[int]] = None,
        fileIds: Optional[List[int]] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[int] = None,
    ):
        """
        Export Project Translation.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.translations.exports.post
        """

        return self.requester.request(
            method="delete",
            path=f"{self.prepare_path(object_id=projectId)}/translations/exports",
            post_data={
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
