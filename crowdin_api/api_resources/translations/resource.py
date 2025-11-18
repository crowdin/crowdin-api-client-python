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
from crowdin_api.decorator import deprecated


class TranslationsResource(BaseResource):
    """
    Resource for Translations.
    
    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Translations
    """

    def get_builds_path(self, projectId: int, buildId: Optional[int] = None):
        if buildId:
            return f"projects/{projectId}/translations/builds/{buildId}"

        return f"projects/{projectId}/translations/builds"

    def get_language_imports_path(self, projectId: int, languageId: str, importId: str):
        return f"projects/{projectId}/languages/{languageId}/imports/{importId}"

    def import_translations(
        self,
        languageId: str,
        storageId: int,
        projectId: Optional[int] = None,
        fileId: Optional[int] = None,
        importEqSuggestions: Optional[bool] = None,
        autoApproveImported: Optional[bool] = None,
        translateHidden: Optional[bool] = None,
    ):
        """
        Import Translations.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.languages.imports.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/languages/{languageId}/imports",
            request_data={
                "storageId": storageId,
                "fileId": fileId,
                "importEqSuggestions": importEqSuggestions,
                "autoApproveImported": autoApproveImported,
                "translateHidden": translateHidden,
            },
        )

    def check_translation_import_status(
        self,
        languageId: str,
        importId: str,
        projectId: Optional[int] = None,
    ):
        """
        Check Translation Import Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.languages.imports.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_language_imports_path(
                projectId=projectId,
                languageId=languageId,
                importId=importId,
            ),
        )

    def download_translation_import_report(
        self,
        languageId: str,
        importId: str,
        projectId: Optional[int] = None,
    ):
        """
        Download Translation Import Report.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.languages.imports.report.download
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=f"{self.get_language_imports_path(projectId, languageId, importId)}/report",
        )

    @deprecated(
        "This method is deprecated in favor of the new 'Import Translations' endpoint. "
        "Link to documentation: "
        "https://developer.crowdin.com/api/v2/#operation/api.projects.languages.imports.post"
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
