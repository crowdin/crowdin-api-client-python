import warnings
from typing import Any, Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import (
    HasManagerAccess,
    ProjectGlossaryAccessOption,
    ProjectLanguageAccessPolicy,
    ProjectTagsDetection,
    ProjectTmContextType,
    ProjectTranslateDuplicates,
    ProjectType,
    ProjectVisibility,
    StringsExporterSettingsPatchPath,
)
from crowdin_api.api_resources.projects.types import (
    AiPreTranslate,
    MtPreTranslate,
    TmPreTranslate,
    WorkflowStepSettings,
    MdFileFormatSettings,
    MdxFileFormatSettings,
    JsonFileFormatSettings,
    JavaScriptFileFormatSettings,
    StringCatalogFileFormatSettings,
    VdfFileFormatSettings,
    StringsExporterSettingsPatchRequest,
    NotificationSettings,
    ProjectPatchRequest,
    QACheckCategories,
    PropertyFileFormatSettings,
    XmlFileFormatSettings,
    DocxFileFormatSettings,
    MediaWikiFileFormatSettings,
    TxtFileFormatSettings,
    OtherFileFormatSettings,
    SpecificFileFormatSettings,
    ProjectFilePatchRequest,
    AndroidStringsExporterSettings,
    MacOSXStringsExporterSettings,
    XliffStringsExporterSettings,
    QAChecksIgnorableCategories
)
from crowdin_api.sorting import Sorting


def _warn_deprecated_project_params(
    glossaryAccess: Optional[bool] = None,
    preTranslationAiPromptId: Optional[int] = None,
):
    if glossaryAccess is not None:
        warnings.warn(
            "`glossaryAccess` is deprecated, use `glossaryAccessOption` instead",
            DeprecationWarning,
        )

    if preTranslationAiPromptId is not None:
        warnings.warn(
            "`preTranslationAiPromptId` is deprecated, use `aiPreTranslate` instead",
            DeprecationWarning,
        )


class ProjectsResource(BaseResource):
    """
    Resource for Storages.

    Using projects, you can keep your source files sorted.
    Use API to manage projects, change their settings, or remove them if required.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Projects

    """

    def get_projects_path(self, projectId: Optional[int] = None):
        if projectId is not None:
            return f"projects/{projectId}"

        return "projects"

    def list_projects(
        self,
        orderBy: Optional[Sorting] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        groupId: Optional[int] = None,
        userId: Optional[Union[int, str]] = None,
        hasManagerAccess: Optional[HasManagerAccess] = None,
        type: Optional[ProjectType] = None,
        filter: Optional[str] = None,
    ):
        """
        List Projects.

        Note: `groupId` is supported by Crowdin Enterprise only, `userId` and `type` by Crowdin only.
        `filter` filters projects by `name`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.getMany
        """

        params = {
            "orderBy": orderBy,
            "userId": userId,
            "hasManagerAccess": hasManagerAccess,
            "groupId": groupId,
            "type": type.value if type is not None else None,
            "filter": filter,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(method="get", path=self.get_projects_path(), params=params)

    def add_project(self, request_data: Dict):
        """
        Add Project.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.post
        """

        return self.requester.request(
            method="post", path=self.get_projects_path(), request_data=request_data
        )

    def add_file_based_project(
        self,
        name: str,
        sourceLanguageId: str,
        type: Optional[ProjectType] = None,
        normalizePlaceholder: Optional[bool] = None,
        saveMetaInfoInSource: Optional[bool] = None,
        notificationSettings: Optional[NotificationSettings] = None,
        identifier: Optional[str] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        visibility: Optional[ProjectVisibility] = None,
        languageAccessPolicy: Optional[ProjectLanguageAccessPolicy] = None,
        cname: Optional[str] = None,
        description: Optional[str] = None,
        translateDuplicates: Optional[ProjectTranslateDuplicates] = None,
        isMtAllowed: Optional[bool] = None,
        autoSubstitution: Optional[bool] = None,
        autoTranslateDialects: Optional[bool] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
        defaultTmId: Optional[int] = None,
        defaultGlossaryId: Optional[int] = None,
        tmApprovedSuggestionsOnly: Optional[bool] = None,
        tagsDetection: Optional[ProjectTagsDetection] = None,
        taskBasedAccessControl: Optional[bool] = None,
        publicDownloads: Optional[bool] = None,
        hiddenStringsProofreadersAccess: Optional[bool] = None,
        useGlobalTm: Optional[bool] = None,
        showTmSuggestionsDialects: Optional[bool] = None,
        qaCheckIsActive: Optional[bool] = None,
        qaCheckCategories: Optional[QACheckCategories] = None,
        qaChecksIgnorableCategories: Optional[QAChecksIgnorableCategories] = None,
        languageMapping: Optional[Dict] = None,
        glossaryAccess: Optional[bool] = None,
        glossaryAccessOption: Optional[ProjectGlossaryAccessOption] = None,
        tmPreTranslate: Optional[TmPreTranslate] = None,
        mtPreTranslate: Optional[MtPreTranslate] = None,
        aiPreTranslate: Optional[AiPreTranslate] = None,
        preTranslationAiPromptId: Optional[int] = None,
        editorSuggestionAiPromptId: Optional[int] = None,
        qaCheckActionAiPromptId: Optional[int] = None,
        contextReviewAiPromptId: Optional[int] = None,
        savingsReportSettingsTemplateId: Optional[int] = None,
        assignedStyleGuides: Optional[Iterable[int]] = None,
        inContext: Optional[bool] = None,
        inContextProcessHiddenStrings: Optional[bool] = None,
        inContextPseudoLanguageId: Optional[str] = None,
        tmContextType: Optional[ProjectTmContextType] = None,
        groupId: Optional[int] = None,
        templateId: Optional[int] = None,
        steps: Optional[Iterable[WorkflowStepSettings]] = None,
        vendorId: Optional[int] = None,
        mtEngineId: Optional[int] = None,
        taskReviewerIds: Optional[Iterable[int]] = None,
        delayedWorkflowStart: Optional[bool] = None,
        exportWithMinApprovalsCount: Optional[int] = None,
        exportStringsThatPassedWorkflow: Optional[bool] = None,
        qaApprovalsCount: Optional[int] = None,
        customQaCheckIds: Optional[Iterable[int]] = None,
        externalQaCheckIds: Optional[Iterable[int]] = None,
        fields: Optional[Dict[str, Any]] = None,
        alignmentActionAiPromptId: Optional[int] = None,
    ):
        """
        Add Project(Files Based Project Form).

        Crowdin only: `identifier`, `visibility`, `languageAccessPolicy`, `cname`,
        `exportApprovedOnly`, `useGlobalTm`, `tmPreTranslate`, `mtPreTranslate`, `aiPreTranslate`.

        Crowdin Enterprise only: `groupId`, `templateId`, `steps`, `vendorId`, `mtEngineId`,
        `taskReviewerIds`, `delayedWorkflowStart`, `exportWithMinApprovalsCount`,
        `exportStringsThatPassedWorkflow`, `qaApprovalsCount`, `customQaCheckIds`,
        `externalQaCheckIds`, `fields`, `alignmentActionAiPromptId`.

        Deprecated: `glossaryAccess` (use `glossaryAccessOption` instead) and
        `preTranslationAiPromptId` (use `aiPreTranslate` instead).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.post
        """

        _warn_deprecated_project_params(
            glossaryAccess=glossaryAccess, preTranslationAiPromptId=preTranslationAiPromptId
        )

        return self.add_project(
            request_data={
                "name": name,
                "sourceLanguageId": sourceLanguageId,
                "identifier": identifier,
                "type": type,
                "normalizePlaceholder": normalizePlaceholder,
                "saveMetaInfoInSource": saveMetaInfoInSource,
                "notificationSettings": notificationSettings,
                "targetLanguageIds": targetLanguageIds,
                "visibility": visibility,
                "languageAccessPolicy": languageAccessPolicy,
                "cname": cname,
                "description": description,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "skipUntranslatedFiles": skipUntranslatedFiles,
                "exportApprovedOnly": exportApprovedOnly,
                "translateDuplicates": translateDuplicates,
                "isMtAllowed": isMtAllowed,
                "autoSubstitution": autoSubstitution,
                "autoTranslateDialects": autoTranslateDialects,
                "defaultTmId": defaultTmId,
                "defaultGlossaryId": defaultGlossaryId,
                "tmApprovedSuggestionsOnly": tmApprovedSuggestionsOnly,
                "tagsDetection": tagsDetection,
                "taskBasedAccessControl": taskBasedAccessControl,
                "publicDownloads": publicDownloads,
                "hiddenStringsProofreadersAccess": hiddenStringsProofreadersAccess,
                "useGlobalTm": useGlobalTm,
                "showTmSuggestionsDialects": showTmSuggestionsDialects,
                "qaCheckIsActive": qaCheckIsActive,
                "qaCheckCategories": qaCheckCategories,
                "qaChecksIgnorableCategories": qaChecksIgnorableCategories,
                "languageMapping": languageMapping,
                "glossaryAccess": glossaryAccess,
                "glossaryAccessOption": glossaryAccessOption,
                "tmPreTranslate": tmPreTranslate,
                "mtPreTranslate": mtPreTranslate,
                "aiPreTranslate": aiPreTranslate,
                "preTranslationAiPromptId": preTranslationAiPromptId,
                "editorSuggestionAiPromptId": editorSuggestionAiPromptId,
                "qaCheckActionAiPromptId": qaCheckActionAiPromptId,
                "contextReviewAiPromptId": contextReviewAiPromptId,
                "savingsReportSettingsTemplateId": savingsReportSettingsTemplateId,
                "assignedStyleGuides": assignedStyleGuides,
                "inContext": inContext,
                "inContextProcessHiddenStrings": inContextProcessHiddenStrings,
                "inContextPseudoLanguageId": inContextPseudoLanguageId,
                "tmContextType": tmContextType,
                "groupId": groupId,
                "templateId": templateId,
                "steps": steps,
                "vendorId": vendorId,
                "mtEngineId": mtEngineId,
                "taskReviewerIds": taskReviewerIds,
                "delayedWorkflowStart": delayedWorkflowStart,
                "exportWithMinApprovalsCount": exportWithMinApprovalsCount,
                "exportStringsThatPassedWorkflow": exportStringsThatPassedWorkflow,
                "qaApprovalsCount": qaApprovalsCount,
                "customQaCheckIds": customQaCheckIds,
                "externalQaCheckIds": externalQaCheckIds,
                "fields": fields,
                "alignmentActionAiPromptId": alignmentActionAiPromptId,
            },
        )

    def add_strings_based_project(
        self,
        name: str,
        sourceLanguageId: str,
        identifier: Optional[str] = None,
        type: Optional[ProjectType] = None,
        targetLanguageIds: Optional[Iterable[str]] = None,
        visibility: Optional[ProjectVisibility] = None,
        languageAccessPolicy: Optional[ProjectLanguageAccessPolicy] = None,
        cname: Optional[str] = None,
        description: Optional[str] = None,
        translateDuplicates: Optional[ProjectTranslateDuplicates] = None,
        isMtAllowed: Optional[bool] = None,
        autoSubstitution: Optional[bool] = None,
        autoTranslateDialects: Optional[bool] = None,
        publicDownloads: Optional[bool] = None,
        hiddenStringsProofreadersAccess: Optional[bool] = None,
        useGlobalTm: Optional[bool] = None,
        skipUntranslatedStrings: Optional[bool] = None,
        skipUntranslatedFiles: Optional[bool] = None,
        exportApprovedOnly: Optional[bool] = None,
        inContextProcessHiddenStrings: Optional[bool] = None,
        inContextPseudoLanguageId: Optional[str] = None,
        qaCheckIsActive: Optional[bool] = None,
        qaCheckCategories: Optional[QACheckCategories] = None,
        qaChecksIgnorableCategories: Optional[QAChecksIgnorableCategories] = None,
        languageMapping: Optional[Dict] = None,
        glossaryAccess: Optional[bool] = None,
        notificationSettings: Optional[NotificationSettings] = None,
        defaultTmId: Optional[int] = None,
        defaultGlossaryId: Optional[int] = None,
        tmApprovedSuggestionsOnly: Optional[bool] = None,
        tagsDetection: Optional[ProjectTagsDetection] = None,
        taskBasedAccessControl: Optional[bool] = None,
        showTmSuggestionsDialects: Optional[bool] = None,
        normalizePlaceholder: Optional[bool] = None,
        glossaryAccessOption: Optional[ProjectGlossaryAccessOption] = None,
        tmPreTranslate: Optional[TmPreTranslate] = None,
        mtPreTranslate: Optional[MtPreTranslate] = None,
        aiPreTranslate: Optional[AiPreTranslate] = None,
        preTranslationAiPromptId: Optional[int] = None,
        editorSuggestionAiPromptId: Optional[int] = None,
        qaCheckActionAiPromptId: Optional[int] = None,
        contextReviewAiPromptId: Optional[int] = None,
        savingsReportSettingsTemplateId: Optional[int] = None,
        assignedStyleGuides: Optional[Iterable[int]] = None,
        inContext: Optional[bool] = None,
        groupId: Optional[int] = None,
        templateId: Optional[int] = None,
        steps: Optional[Iterable[WorkflowStepSettings]] = None,
        vendorId: Optional[int] = None,
        mtEngineId: Optional[int] = None,
        taskReviewerIds: Optional[Iterable[int]] = None,
        delayedWorkflowStart: Optional[bool] = None,
        exportWithMinApprovalsCount: Optional[int] = None,
        exportStringsThatPassedWorkflow: Optional[bool] = None,
        qaApprovalsCount: Optional[int] = None,
        customQaCheckIds: Optional[Iterable[int]] = None,
        externalQaCheckIds: Optional[Iterable[int]] = None,
        fields: Optional[Dict[str, Any]] = None,
        alignmentActionAiPromptId: Optional[int] = None,
    ):
        """
        Add Project(Strings Based Project Form).

        Crowdin only: `identifier`, `visibility`, `languageAccessPolicy`, `cname`,
        `exportApprovedOnly`, `useGlobalTm`, `tmPreTranslate`, `mtPreTranslate`, `aiPreTranslate`.

        Crowdin Enterprise only: `groupId`, `templateId`, `steps`, `vendorId`, `mtEngineId`,
        `taskReviewerIds`, `delayedWorkflowStart`, `exportWithMinApprovalsCount`,
        `exportStringsThatPassedWorkflow`, `qaApprovalsCount`, `customQaCheckIds`,
        `externalQaCheckIds`, `fields`, `alignmentActionAiPromptId`.

        Deprecated: `glossaryAccess` (use `glossaryAccessOption` instead) and
        `preTranslationAiPromptId` (use `aiPreTranslate` instead).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/string-based/#operation/api.projects.post
        """

        _warn_deprecated_project_params(
            glossaryAccess=glossaryAccess, preTranslationAiPromptId=preTranslationAiPromptId
        )

        return self.add_project(
            request_data={
                "name": name,
                "sourceLanguageId": sourceLanguageId,
                "identifier": identifier,
                "type": type,
                "targetLanguageIds": targetLanguageIds,
                "visibility": visibility,
                "languageAccessPolicy": languageAccessPolicy,
                "cname": cname,
                "description": description,
                "skipUntranslatedStrings": skipUntranslatedStrings,
                "skipUntranslatedFiles": skipUntranslatedFiles,
                "exportApprovedOnly": exportApprovedOnly,
                "translateDuplicates": translateDuplicates,
                "isMtAllowed": isMtAllowed,
                "autoSubstitution": autoSubstitution,
                "autoTranslateDialects": autoTranslateDialects,
                "publicDownloads": publicDownloads,
                "hiddenStringsProofreadersAccess": hiddenStringsProofreadersAccess,
                "useGlobalTm": useGlobalTm,
                "inContextProcessHiddenStrings": inContextProcessHiddenStrings,
                "inContextPseudoLanguageId": inContextPseudoLanguageId,
                "qaCheckIsActive": qaCheckIsActive,
                "qaCheckCategories": qaCheckCategories,
                "qaChecksIgnorableCategories": qaChecksIgnorableCategories,
                "languageMapping": languageMapping,
                "glossaryAccess": glossaryAccess,
                "notificationSettings": notificationSettings,
                "defaultTmId": defaultTmId,
                "defaultGlossaryId": defaultGlossaryId,
                "tmApprovedSuggestionsOnly": tmApprovedSuggestionsOnly,
                "tagsDetection": tagsDetection,
                "taskBasedAccessControl": taskBasedAccessControl,
                "showTmSuggestionsDialects": showTmSuggestionsDialects,
                "normalizePlaceholder": normalizePlaceholder,
                "glossaryAccessOption": glossaryAccessOption,
                "tmPreTranslate": tmPreTranslate,
                "mtPreTranslate": mtPreTranslate,
                "aiPreTranslate": aiPreTranslate,
                "preTranslationAiPromptId": preTranslationAiPromptId,
                "editorSuggestionAiPromptId": editorSuggestionAiPromptId,
                "qaCheckActionAiPromptId": qaCheckActionAiPromptId,
                "contextReviewAiPromptId": contextReviewAiPromptId,
                "savingsReportSettingsTemplateId": savingsReportSettingsTemplateId,
                "assignedStyleGuides": assignedStyleGuides,
                "inContext": inContext,
                "groupId": groupId,
                "templateId": templateId,
                "steps": steps,
                "vendorId": vendorId,
                "mtEngineId": mtEngineId,
                "taskReviewerIds": taskReviewerIds,
                "delayedWorkflowStart": delayedWorkflowStart,
                "exportWithMinApprovalsCount": exportWithMinApprovalsCount,
                "exportStringsThatPassedWorkflow": exportStringsThatPassedWorkflow,
                "qaApprovalsCount": qaApprovalsCount,
                "customQaCheckIds": customQaCheckIds,
                "externalQaCheckIds": externalQaCheckIds,
                "fields": fields,
                "alignmentActionAiPromptId": alignmentActionAiPromptId,
            },
        )

    def get_project(self, projectId: Optional[int] = None):
        """
        Get Project.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get", path=self.get_projects_path(projectId=projectId)
        )

    def delete_project(self, projectId: Optional[int] = None):
        """
        Delete Project.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete", path=self.get_projects_path(projectId=projectId)
        )

    def edit_project(
        self, data: Iterable[ProjectPatchRequest], projectId: Optional[int] = None
    ):
        """
        Edit Project.

        See `ProjectPatchPath` for the available paths, including the Crowdin Enterprise only
        and file-based only ones.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_projects_path(projectId=projectId),
            request_data=data,
        )

    def get_project_file_format_settings_path(
        self,
        projectId: int,
        fileFormatSettingsId: Optional[int] = None
    ):
        if fileFormatSettingsId is not None:
            return f"projects/{projectId}/file-format-settings/{fileFormatSettingsId}"

        return f"projects/{projectId}/file-format-settings"

    def download_project_file_custom_segmentation(
        self, fileFormatSettingsId: int, projectId: Optional[int] = None
    ):
        """
        Download Project File Format Settings Custom Segmentation.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.file-format-settings.custom-segmentations.get
        """

        projectId = projectId or self.get_project_id()

        path = self.get_project_file_format_settings_path(
            projectId=projectId,
            fileFormatSettingsId=fileFormatSettingsId
        )

        return self.requester.request(
            method="get",
            path=f"{path}/custom-segmentations",
        )

    def reset_project_file_custom_segmentation(
        self, fileFormatSettingsId: int, projectId: Optional[int] = None
    ):
        """
        Reset Project File Format Settings Custom Segmentation.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.file-format-settings.custom-segmentations.delete
        """

        projectId = projectId or self.get_project_id()
        path = self.get_project_file_format_settings_path(
            projectId=projectId,
            fileFormatSettingsId=fileFormatSettingsId
        )

        return self.requester.request(
            method="delete",
            path=f"{path}/custom-segmentations",
        )

    def list_project_file_format_settings(
        self,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Project File Format Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.file-format-settings.getMany
        """

        projectId = projectId or self.get_project_id()
        params = self.get_page_params(page=page, offset=offset, limit=limit)

        return self._get_entire_data(
            method="get",
            path=self.get_project_file_format_settings_path(projectId=projectId),
            params=params
        )

    def add_project_file_format_settings(
        self,
        format: str,
        settings: Union[
            PropertyFileFormatSettings, XmlFileFormatSettings, SpecificFileFormatSettings,
            DocxFileFormatSettings, MediaWikiFileFormatSettings, TxtFileFormatSettings,
            OtherFileFormatSettings, MdFileFormatSettings, MdxFileFormatSettings,
            JsonFileFormatSettings, JavaScriptFileFormatSettings, StringCatalogFileFormatSettings,
            VdfFileFormatSettings, Dict[str, Any]
        ],
        projectId: Optional[int] = None,
    ):
        """
        Add Project File Format Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.file-format-settings.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_project_file_format_settings_path(projectId=projectId),
            request_data={"format": format, "settings": settings}
        )

    def get_project_file_format_settings(
        self, fileFormatSettingsId: int, projectId: Optional[int] = None
    ):
        """
        Get Project File Format Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.file-format-settings.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_project_file_format_settings_path(
                projectId=projectId,
                fileFormatSettingsId=fileFormatSettingsId
            ),
        )

    def delete_project_file_format_settings(
        self, fileFormatSettingsId: int, projectId: Optional[int] = None
    ):
        """
        Delete Project File Format Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.file-format-settings.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_project_file_format_settings_path(
                projectId=projectId,
                fileFormatSettingsId=fileFormatSettingsId
            ),
        )

    def edit_project_file_format_settings(
        self,
        fileFormatSettingsId: int,
        data: Iterable[ProjectFilePatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Project File Format Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.file-format-settings.patch
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_project_file_format_settings_path(
                projectId=projectId,
                fileFormatSettingsId=fileFormatSettingsId
            ),
            request_data=data,
        )

    def get_strings_exporter_path(
        self,
        projectId: int,
        systemStringExporterSettingsId: Optional[int] = None
    ):
        if systemStringExporterSettingsId is None:
            return f"projects/{projectId}/strings-exporter-settings"
        return f"projects/{projectId}/strings-exporter-settings/{systemStringExporterSettingsId}"

    def list_project_strings_exporter_settings(
        self,
        projectId: Optional[int] = None,
    ):
        """
        List Project Strings Exporter Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings-exporter-settings.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_strings_exporter_path(projectId=projectId),
        )

    def add_project_strings_exporter_settings(
        self,
        format: str,
        settings: Union[
            AndroidStringsExporterSettings,
            MacOSXStringsExporterSettings,
            XliffStringsExporterSettings,
        ],
        projectId: Optional[int] = None,
    ):
        """
        Add Project Strings Exporter Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings-exporter-settings.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_strings_exporter_path(projectId=projectId),
            request_data={"format": format, "settings": settings},
        )

    def get_project_strings_exporter_settings(
        self, systemStringExporterSettingsId: int, projectId: Optional[int] = None
    ):
        """
        Get Project Strings Exporter Settings

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings-exporter-settings.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_strings_exporter_path(
                projectId=projectId,
                systemStringExporterSettingsId=systemStringExporterSettingsId,
            ),
        )

    def delete_project_strings_exporter_settings(
        self, systemStringExporterSettingsId: int, projectId: Optional[int] = None
    ):
        """
        Delete Project Strings Exporter Settings.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings-exporter-settings.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_strings_exporter_path(
                projectId=projectId,
                systemStringExporterSettingsId=systemStringExporterSettingsId,
            ),
        )

    def edit_project_strings_exporter_settings(
        self,
        systemStringExporterSettingsId: int,
        format: Optional[str] = None,
        settings: Optional[Union[
            AndroidStringsExporterSettings,
            MacOSXStringsExporterSettings,
            XliffStringsExporterSettings,
        ]] = None,
        projectId: Optional[int] = None,
        data: Optional[Iterable[StringsExporterSettingsPatchRequest]] = None,
    ):
        """
        Edit Project Strings Exporter Settings.

        The API expects a JSON Patch document. Pass it via `data`, or pass `format` and/or
        `settings` and they will be sent as `replace` operations on `/format` and `/settings`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.strings-exporter-settings.patch
        """

        projectId = projectId or self.get_project_id()

        if data is None:
            data = []
            if format is not None:
                data.append(
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": StringsExporterSettingsPatchPath.FORMAT.value,
                        "value": format,
                    }
                )
            if settings is not None:
                data.append(
                    {
                        "op": PatchOperation.REPLACE.value,
                        "path": StringsExporterSettingsPatchPath.SETTINGS.value,
                        "value": settings,
                    }
                )

        return self.requester.request(
            method="patch",
            path=self.get_strings_exporter_path(
                projectId=projectId,
                systemStringExporterSettingsId=systemStringExporterSettingsId
            ),
            request_data=data,
        )
