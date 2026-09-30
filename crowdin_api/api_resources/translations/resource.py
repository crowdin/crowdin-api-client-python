import warnings
from typing import Dict, Iterable, Optional

from deprecated import deprecated

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import ExportProjectTranslationFormat
from crowdin_api.api_resources.translations.types import (
    FallbackLanguages,
    EditPreTranslationScheme,
    ImportTranslationsOptions,
    UploadTranslationRequest,
)
from crowdin_api.api_resources.translations.enums import (
    CharTransformation,
    PreTranslationApplyMethod,
    PreTranslationAutoApproveOption,
    PreTranslationPriority,
    PreTranslationReplaceTranslationsOption,
    PreTranslationScope,
)
from crowdin_api.sorting import Sorting


class TranslationsResource(BaseResource):
    """
    Resource for Translations.

    Translators can work with entirely untranslated project or you can pre-translate the files to
    ease the translations process.

    Use API to pre-translate files via Machine Translation (MT) or Translation Memory (TM), upload
    your existing translations, and download translations correspondingly. Pre-translate and build
    are asynchronous operations and shall be completed with sequence of API methods.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Translations
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

        `preTranslationId` is the auto-translation job identifier (`jobIdentifier` in the API reference).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/paths/~1projects~1{projectId}~1pre-translations~1{preTranslationId}/get
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
        orderBy: Optional[Sorting] = None,
    ):
        """
        List Pre-Translations

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.pre-translations.getMany
        """
        projectId = projectId or self.get_project_id()

        params = {"orderBy": orderBy}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/pre-translations",
            params=params,
        )

    def apply_pre_translation(
        self,
        languageIds: Optional[Iterable[str]] = None,
        fileIds: Optional[Iterable[int]] = None,
        projectId: Optional[int] = None,
        method: Optional[PreTranslationApplyMethod] = None,
        engineId: Optional[int] = None,
        aiPromptId: Optional[int] = None,
        autoApproveOption: Optional[PreTranslationAutoApproveOption] = None,
        duplicateTranslations: Optional[bool] = None,
        skipApprovedTranslations: Optional[bool] = None,
        translateUntranslatedOnly: Optional[bool] = None,
        scope: Optional[PreTranslationScope] = None,
        translationModifiedBefore: Optional[str] = None,
        replaceTranslationsOption: Optional[PreTranslationReplaceTranslationsOption] = None,
        resetApprovalStatus: Optional[bool] = None,
        translateWithPerfectMatchOnly: Optional[bool] = None,
        fallbackLanguages: Optional[Iterable[FallbackLanguages]] = None,
        labelIds: Optional[Iterable[int]] = None,
        excludeLabelIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
        directoryIds: Optional[Iterable[int]] = None,
        taskId: Optional[int] = None,
        priority: Optional[PreTranslationPriority] = None,
        translationModifiedAfter: Optional[str] = None,
        notifyOnCompletion: Optional[bool] = None,
        sourceLanguageId: Optional[str] = None,
        customInstruction: Optional[str] = None,
        minimumMatchRatio: Optional[int] = None,
    ):
        """
        Apply Pre-Translation.

        Pre-translate by files: pass `languageIds` together with `fileIds`, `directoryIds`
        (file-based projects only) or `branchIds`. `fileIds` is required only when neither
        `directoryIds` nor `branchIds` is set.

        Pre-translate by task: pass `taskId` (the target language is taken from the task),
        `languageIds` and files are not required in this case.

        `translateUntranslatedOnly` is deprecated in favor of `scope` and cannot be
        combined with it in the same request.

        `sourceLanguageId` is available in Crowdin only, `minimumMatchRatio` in
        Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.pre-translations.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.pre-translations.post
        """
        if translateUntranslatedOnly is not None and scope is not None:
            raise ValueError(
                "translateUntranslatedOnly is deprecated in favor of scope and "
                "cannot be combined with it in the same request."
            )

        if translateUntranslatedOnly is not None:
            warnings.warn(
                "`translateUntranslatedOnly` is deprecated, use `scope` instead",
                DeprecationWarning,
            )

        if fallbackLanguages is None:
            fallbackLanguages = []

        if labelIds is None:
            labelIds = []

        if excludeLabelIds is None:
            excludeLabelIds = []

        if branchIds is None:
            branchIds = []

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
                "scope": scope,
                "translationModifiedBefore": translationModifiedBefore,
                "replaceTranslationsOption": replaceTranslationsOption,
                "resetApprovalStatus": resetApprovalStatus,
                "translateWithPerfectMatchOnly": translateWithPerfectMatchOnly,
                "fallbackLanguages": fallbackLanguages,
                "labelIds": labelIds,
                "excludeLabelIds": excludeLabelIds,
                "branchIds": branchIds,
                "directoryIds": directoryIds,
                "taskId": taskId,
                "priority": priority,
                "translationModifiedAfter": translationModifiedAfter,
                "notifyOnCompletion": notifyOnCompletion,
                "sourceLanguageId": sourceLanguageId,
                "customInstruction": customInstruction,
                "minimumMatchRatio": minimumMatchRatio,
            },
        )

    def pre_translation_report(
        self,
        preTranslationId: str,
        projectId: Optional[int] = None,
    ):
        """
        Pre-Translation Report

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.pre-translations.report.getReport
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=f"projects/{projectId}/pre-translations/{preTranslationId}/report",
        )

    def edit_pre_translation(
        self,
        preTranslationId: str,
        data: Iterable[EditPreTranslationScheme],
        projectId: Optional[int] = None,
    ):
        """
        Edit Pre-Translation

        Supported patch paths: `PreTranslationPatchPath` (`/status`, `/priority`).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.pre-translations.patch
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=f"projects/{projectId}/pre-translations/{preTranslationId}",
            request_data=data,
        )

    def pre_translation_batch_operations(
        self,
        data: Iterable[EditPreTranslationScheme],
        projectId: Optional[int] = None,
    ):
        """
        Pre-Translation Batch Operations.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.pre-translations.patchBatch
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=f"projects/{projectId}/pre-translations",
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
        exportWithMinApprovalsCount: Optional[int] = None,
        exportStringsThatPassedWorkflow: Optional[bool] = None,
        preserveFolderHierarchy: Optional[bool] = None,
    ):
        """
        Build Project Directory Translation.

        `exportApprovedOnly` is available in Crowdin only; `exportWithMinApprovalsCount` and
        `exportStringsThatPassedWorkflow` in Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.directories.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.translations.builds.directories.post
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
                "exportWithMinApprovalsCount": exportWithMinApprovalsCount,
                "exportStringsThatPassedWorkflow": exportStringsThatPassedWorkflow,
                "preserveFolderHierarchy": preserveFolderHierarchy,
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
        exportWithMinApprovalsCount: Optional[int] = None,
        exportStringsThatPassedWorkflow: Optional[bool] = None,
    ):
        """
        Build Project File Translation.

        `exportApprovedOnly` is available in Crowdin only; `exportWithMinApprovalsCount` and
        `exportStringsThatPassedWorkflow` in Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.files.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.translations.builds.files.post
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
                "exportWithMinApprovalsCount": exportWithMinApprovalsCount,
                "exportStringsThatPassedWorkflow": exportStringsThatPassedWorkflow,
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.getMany
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.post
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
        exportStringsThatPassedWorkflow: Optional[bool] = None,
    ):
        """
        Build Project Translation(Crowdin Translation Create Project Build Form).

        File-based projects only. `exportApprovedOnly` is available in Crowdin only;
        `exportWithMinApprovalsCount` and `exportStringsThatPassedWorkflow` in Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.translations.builds.post
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
                "exportStringsThatPassedWorkflow": exportStringsThatPassedWorkflow,
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
        branchId: Optional[int] = None,
    ):
        """
        Build Project Translation(Translation Create Project Pseudo Build Form).

        File-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.post
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
                "branchId": branchId,
            },
        )

    @deprecated("Use `import_translations` instead")
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

        Deprecated by the API: use `import_translations` instead.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.postOnLanguage
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.download.download
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.get
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.builds.delete
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
        exportWithMinApprovalsCount: Optional[int] = None,
        exportStringsThatPassedWorkflow: Optional[bool] = None,
    ):
        """
        Export Project Translation.

        `directoryIds`, `fileIds` and `skipUntranslatedFiles` are available in file-based projects only.
        `exportApprovedOnly` is available in Crowdin only; `exportWithMinApprovalsCount` and
        `exportStringsThatPassedWorkflow` in Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.exports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.translations.exports.post
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
                "exportWithMinApprovalsCount": exportWithMinApprovalsCount,
                "exportStringsThatPassedWorkflow": exportStringsThatPassedWorkflow,
            },
        )

    def import_translations(
        self,
        project_id: int,
        storage_id: int,
        language_ids: Optional[Iterable[str]] = None,
        file_id: Optional[int] = None,
        import_eq_suggestions: Optional[bool] = None,
        auto_approve_imported: Optional[bool] = None,
        translate_hidden: Optional[bool] = None,
        add_to_tm: Optional[bool] = None,
        branch_id: Optional[int] = None,
        import_options: Optional[ImportTranslationsOptions] = None,
    ):
        """
        Import Translations

        `file_id` is used in file-based projects; `branch_id` and `import_options`
        (spreadsheet columns mapping) in string-based projects.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.translations.imports
        """

        return self.requester.request(
            method="post",
            path=f"projects/{project_id}/translations/imports",
            request_data={
                "storageId": storage_id,
                "languageIds": language_ids,
                "fileId": file_id,
                "importEqSuggestions": import_eq_suggestions,
                "autoApproveImported": auto_approve_imported,
                "translateHidden": translate_hidden,
                "addToTm": add_to_tm,
                "branchId": branch_id,
                "importOptions": import_options,
            }
        )

    def import_translations_status(
        self,
        project_id: int,
        import_translation_id: int
    ):
        """
        Import Translations Status

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.translations.imports.get
        """

        return self.requester.request(
            method="get",
            path=f"projects/{project_id}/translations/imports/{import_translation_id}",
        )

    def import_translations_report(
        self,
        project_id: int,
        import_translation_id: int,
    ):
        """
        Import Translations Report

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translations/operation/api.projects.translations.imports.report.get
        """

        return self.requester.request(
            method="get",
            path=f"projects/{project_id}/translations/imports/{import_translation_id}/report",
        )
