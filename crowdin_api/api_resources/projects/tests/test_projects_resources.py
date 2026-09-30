from unittest import mock

import pytest
from crowdin_api.api_resources import ProjectsResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import (
    HasManagerAccess,
    ListProjectsOrderBy,
    ProjectGlossaryAccessOption,
    ProjectTagsDetection,
    ProjectTmContextType,
    StringsExporterSettingsPatchPath,
    TmPreTranslateAutoApproveOption,
    TmPreTranslateMinimumMatchRatio,
    ProjectLanguageAccessPolicy,
    ProjectPatchPath,
    ProjectTranslateDuplicates,
    ProjectType,
    ProjectVisibility,
    ProjectFilePatchPath,
)
from crowdin_api.api_resources.projects.types import (
    NotificationSettings,
    QACheckCategories,
    QAChecksIgnorableCategories
)
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule

FILE_BASED_NEW_FIELDS = {
    "tagsDetection": None,
    "taskBasedAccessControl": None,
    "showTmSuggestionsDialects": None,
    "glossaryAccessOption": None,
    "tmPreTranslate": None,
    "mtPreTranslate": None,
    "aiPreTranslate": None,
    "preTranslationAiPromptId": None,
    "editorSuggestionAiPromptId": None,
    "qaCheckActionAiPromptId": None,
    "contextReviewAiPromptId": None,
    "savingsReportSettingsTemplateId": None,
    "assignedStyleGuides": None,
    "inContext": None,
    "groupId": None,
    "templateId": None,
    "steps": None,
    "vendorId": None,
    "mtEngineId": None,
    "taskReviewerIds": None,
    "delayedWorkflowStart": None,
    "exportWithMinApprovalsCount": None,
    "exportStringsThatPassedWorkflow": None,
    "qaApprovalsCount": None,
    "customQaCheckIds": None,
    "externalQaCheckIds": None,
    "fields": None,
    "alignmentActionAiPromptId": None,
    "publicDownloads": None,
    "hiddenStringsProofreadersAccess": None,
    "useGlobalTm": None,
    "qaCheckIsActive": None,
    "qaCheckCategories": None,
    "qaChecksIgnorableCategories": None,
    "languageMapping": None,
    "glossaryAccess": None,
    "inContextProcessHiddenStrings": None,
    "inContextPseudoLanguageId": None,
    "tmContextType": None,
}

STRINGS_BASED_NEW_FIELDS = {
    "tagsDetection": None,
    "taskBasedAccessControl": None,
    "showTmSuggestionsDialects": None,
    "glossaryAccessOption": None,
    "tmPreTranslate": None,
    "mtPreTranslate": None,
    "aiPreTranslate": None,
    "preTranslationAiPromptId": None,
    "editorSuggestionAiPromptId": None,
    "qaCheckActionAiPromptId": None,
    "contextReviewAiPromptId": None,
    "savingsReportSettingsTemplateId": None,
    "assignedStyleGuides": None,
    "inContext": None,
    "groupId": None,
    "templateId": None,
    "steps": None,
    "vendorId": None,
    "mtEngineId": None,
    "taskReviewerIds": None,
    "delayedWorkflowStart": None,
    "exportWithMinApprovalsCount": None,
    "exportStringsThatPassedWorkflow": None,
    "qaApprovalsCount": None,
    "customQaCheckIds": None,
    "externalQaCheckIds": None,
    "fields": None,
    "alignmentActionAiPromptId": None,
    "normalizePlaceholder": None,
}

ADD_FILE_BASED_PROJECT_BASE_FIELDS = (
    "identifier",
    "type",
    "normalizePlaceholder",
    "saveMetaInfoInSource",
    "notificationSettings",
    "targetLanguageIds",
    "visibility",
    "languageAccessPolicy",
    "cname",
    "description",
    "skipUntranslatedStrings",
    "skipUntranslatedFiles",
    "exportApprovedOnly",
    "translateDuplicates",
    "isMtAllowed",
    "autoSubstitution",
    "autoTranslateDialects",
    "defaultTmId",
    "defaultGlossaryId",
    "tmApprovedSuggestionsOnly",
)

ADD_STRINGS_BASED_PROJECT_BASE_FIELDS = (
    "identifier",
    "type",
    "targetLanguageIds",
    "visibility",
    "languageAccessPolicy",
    "cname",
    "description",
    "skipUntranslatedStrings",
    "skipUntranslatedFiles",
    "exportApprovedOnly",
    "translateDuplicates",
    "isMtAllowed",
    "autoSubstitution",
    "autoTranslateDialects",
    "publicDownloads",
    "hiddenStringsProofreadersAccess",
    "useGlobalTm",
    "inContextProcessHiddenStrings",
    "inContextPseudoLanguageId",
    "qaCheckIsActive",
    "qaCheckCategories",
    "qaChecksIgnorableCategories",
    "languageMapping",
    "glossaryAccess",
    "notificationSettings",
    "defaultTmId",
    "defaultGlossaryId",
    "tmApprovedSuggestionsOnly",
)


class TestProjectsResource:
    resource_class = ProjectsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "projectId, path",
        (
            (None, "projects"),
            (1, "projects/1"),
        ),
    )
    def test_get_projects_path(self, projectId, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_projects_path(projectId=projectId) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "orderBy": Sorting(
                        [SortingRule(ListProjectsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "userId": 1,
                    "groupId": 1,
                    "hasManagerAccess": HasManagerAccess.TRUE,
                    "type": ProjectType.STRING_BASED,
                    "filter": "name",
                },
                {
                    "orderBy": Sorting(
                        [SortingRule(ListProjectsOrderBy.ID, SortingOrder.DESC)]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "userId": 1,
                    "groupId": 1,
                    "hasManagerAccess": HasManagerAccess.TRUE,
                    "type": 1,
                    "filter": "name",
                },
            ),
            (
                {"offset": 0, "limit": 10},
                {
                    "orderBy": None,
                    "offset": 0,
                    "limit": 10,
                    "userId": None,
                    "groupId": None,
                    "hasManagerAccess": None,
                    "type": None,
                    "filter": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_projects(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_projects(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path="projects",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_project(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_project(request_data={"some_key": "some_value"}) == "response"
        m_request.assert_called_once_with(
            method="post",
            request_data={"some_key": "some_value"},
            path=resource.get_projects_path(),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "name": "name",
                    "sourceLanguageId": "ua",
                },
                {
                    **FILE_BASED_NEW_FIELDS,
                    "name": "name",
                    "sourceLanguageId": "ua",
                    "identifier": None,
                    "type": None,
                    "normalizePlaceholder": None,
                    "saveMetaInfoInSource": None,
                    "targetLanguageIds": None,
                    "visibility": None,
                    "languageAccessPolicy": None,
                    "cname": None,
                    "description": None,
                    "skipUntranslatedStrings": None,
                    "skipUntranslatedFiles": None,
                    "exportApprovedOnly": None,
                    "translateDuplicates": None,
                    "isMtAllowed": None,
                    "autoSubstitution": None,
                    "autoTranslateDialects": None,
                    "notificationSettings": None,
                    "defaultTmId": None,
                    "defaultGlossaryId": None,
                    "tmApprovedSuggestionsOnly": None,
                },
            ),
            (
                {
                    "name": "name",
                    "sourceLanguageId": "ua",
                    "identifier": "identifier",
                    "type": ProjectType.STRING_BASED,
                    "normalizePlaceholder": True,
                    "saveMetaInfoInSource": True,
                    "targetLanguageIds": ["ua", "en"],
                    "visibility": ProjectVisibility.OPEN,
                    "languageAccessPolicy": ProjectLanguageAccessPolicy.MODERATE,
                    "cname": "cname",
                    "description": "description",
                    "skipUntranslatedStrings": "skipUntranslatedStrings",
                    "skipUntranslatedFiles": "skipUntranslatedFiles",
                    "exportApprovedOnly": "exportApprovedOnly",
                    "translateDuplicates": ProjectTranslateDuplicates.SHOW,
                    "isMtAllowed": True,
                    "autoSubstitution": True,
                    "autoTranslateDialects": True,
                    "notificationSettings": NotificationSettings(
                        translatorNewStrings=True,
                        managerNewStrings=True,
                        managerLanguageCompleted=True,
                    ),
                    "defaultTmId": 1,
                    "defaultGlossaryId": 1,
                    "tmApprovedSuggestionsOnly": True,
                },
                {
                    **FILE_BASED_NEW_FIELDS,
                    "name": "name",
                    "sourceLanguageId": "ua",
                    "identifier": "identifier",
                    "type": ProjectType.STRING_BASED,
                    "normalizePlaceholder": True,
                    "saveMetaInfoInSource": True,
                    "targetLanguageIds": ["ua", "en"],
                    "visibility": ProjectVisibility.OPEN,
                    "languageAccessPolicy": ProjectLanguageAccessPolicy.MODERATE,
                    "cname": "cname",
                    "description": "description",
                    "skipUntranslatedStrings": "skipUntranslatedStrings",
                    "skipUntranslatedFiles": "skipUntranslatedFiles",
                    "exportApprovedOnly": "exportApprovedOnly",
                    "translateDuplicates": ProjectTranslateDuplicates.SHOW,
                    "isMtAllowed": True,
                    "autoSubstitution": True,
                    "autoTranslateDialects": True,
                    "notificationSettings": NotificationSettings(
                        translatorNewStrings=True,
                        managerNewStrings=True,
                        managerLanguageCompleted=True,
                    ),
                    "defaultTmId": 1,
                    "defaultGlossaryId": 1,
                    "tmApprovedSuggestionsOnly": True,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.projects.resource.ProjectsResource.add_project")
    def test_add_file_based_project(self, m_add_project, in_params, request_data, base_absolut_url):
        m_add_project.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_file_based_project(**in_params) == "response"
        m_add_project.assert_called_once_with(request_data=request_data)

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "name": "name",
                    "sourceLanguageId": "ua",
                },
                {
                    **STRINGS_BASED_NEW_FIELDS,
                    "name": "name",
                    "sourceLanguageId": "ua",
                    "identifier": None,
                    "type": None,
                    "targetLanguageIds": None,
                    "visibility": None,
                    "languageAccessPolicy": None,
                    "cname": None,
                    "description": None,
                    "skipUntranslatedStrings": None,
                    "skipUntranslatedFiles": None,
                    "exportApprovedOnly": None,
                    "translateDuplicates": None,
                    "isMtAllowed": None,
                    "autoSubstitution": None,
                    "autoTranslateDialects": None,
                    "publicDownloads": None,
                    "hiddenStringsProofreadersAccess": None,
                    "useGlobalTm": None,
                    "inContextProcessHiddenStrings": None,
                    "inContextPseudoLanguageId": None,
                    "qaCheckIsActive": None,
                    "qaCheckCategories": None,
                    "qaChecksIgnorableCategories": None,
                    "languageMapping": None,
                    "glossaryAccess": None,
                    "notificationSettings": None,
                    "defaultTmId": None,
                    "defaultGlossaryId": None,
                    "tmApprovedSuggestionsOnly": None,
                },
            ),
            (
                {
                    "name": "name",
                    "sourceLanguageId": "ua",
                    "identifier": "identifier",
                    "type": ProjectType.STRING_BASED,
                    "targetLanguageIds": ["ua", "en"],
                    "visibility": ProjectVisibility.OPEN,
                    "languageAccessPolicy": ProjectLanguageAccessPolicy.MODERATE,
                    "cname": "cname",
                    "description": "description",
                    "skipUntranslatedStrings": "skipUntranslatedStrings",
                    "skipUntranslatedFiles": "skipUntranslatedFiles",
                    "exportApprovedOnly": "exportApprovedOnly",
                    "translateDuplicates": ProjectTranslateDuplicates.SHOW,
                    "isMtAllowed": True,
                    "autoSubstitution": True,
                    "autoTranslateDialects": True,
                    "publicDownloads": True,
                    "hiddenStringsProofreadersAccess": True,
                    "useGlobalTm": True,
                    "inContextProcessHiddenStrings": True,
                    "inContextPseudoLanguageId": "ua",
                    "qaCheckIsActive": True,
                    "qaCheckCategories": QACheckCategories(
                        empty=True,
                        size=True,
                        tags=True,
                        spaces=True,
                        variables=True,
                        punctuation=True,
                        symbolRegister=True,
                        specialSymbols=True,
                        wrongTranslation=True,
                        spellcheck=True,
                        icu=True,
                        terms=True,
                        duplicate=True,
                    ),
                    "qaChecksIgnorableCategories": QAChecksIgnorableCategories(
                        empty=True,
                        size=True,
                        tags=True,
                        spaces=True,
                        variables=True,
                        punctuation=True,
                        symbolRegister=True,
                        specialSymbols=True,
                        wrongTranslation=True,
                        spellcheck=True,
                        icu=True,
                        terms=True,
                        duplicate=True,
                        ftl=True,
                        android=True
                    ),
                    "languageMapping": {},
                    "glossaryAccess": True,
                    "notificationSettings": NotificationSettings(
                        translatorNewStrings=True,
                        managerNewStrings=True,
                        managerLanguageCompleted=True,
                    ),
                    "defaultTmId": 1,
                    "defaultGlossaryId": 1,
                    "tmApprovedSuggestionsOnly": True,
                },
                {
                    **STRINGS_BASED_NEW_FIELDS,
                    "name": "name",
                    "sourceLanguageId": "ua",
                    "identifier": "identifier",
                    "type": ProjectType.STRING_BASED,
                    "targetLanguageIds": ["ua", "en"],
                    "visibility": ProjectVisibility.OPEN,
                    "languageAccessPolicy": ProjectLanguageAccessPolicy.MODERATE,
                    "cname": "cname",
                    "description": "description",
                    "skipUntranslatedStrings": "skipUntranslatedStrings",
                    "skipUntranslatedFiles": "skipUntranslatedFiles",
                    "exportApprovedOnly": "exportApprovedOnly",
                    "translateDuplicates": ProjectTranslateDuplicates.SHOW,
                    "isMtAllowed": True,
                    "autoSubstitution": True,
                    "autoTranslateDialects": True,
                    "publicDownloads": True,
                    "hiddenStringsProofreadersAccess": True,
                    "useGlobalTm": True,
                    "inContextProcessHiddenStrings": True,
                    "inContextPseudoLanguageId": "ua",
                    "qaCheckIsActive": True,
                    "qaCheckCategories": QACheckCategories(
                        empty=True,
                        size=True,
                        tags=True,
                        spaces=True,
                        variables=True,
                        punctuation=True,
                        symbolRegister=True,
                        specialSymbols=True,
                        wrongTranslation=True,
                        spellcheck=True,
                        icu=True,
                        terms=True,
                        duplicate=True,
                    ),
                    "qaChecksIgnorableCategories": QAChecksIgnorableCategories(
                        empty=True,
                        size=True,
                        tags=True,
                        spaces=True,
                        variables=True,
                        punctuation=True,
                        symbolRegister=True,
                        specialSymbols=True,
                        wrongTranslation=True,
                        spellcheck=True,
                        icu=True,
                        terms=True,
                        duplicate=True,
                        ftl=True,
                        android=True,
                    ),
                    "languageMapping": {},
                    "glossaryAccess": True,
                    "notificationSettings": NotificationSettings(
                        translatorNewStrings=True,
                        managerNewStrings=True,
                        managerLanguageCompleted=True,
                    ),
                    "defaultTmId": 1,
                    "defaultGlossaryId": 1,
                    "tmApprovedSuggestionsOnly": True,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.projects.resource.ProjectsResource.add_project")
    def test_add_strings_based_projectt(
        self, m_add_project, in_params, request_data, base_absolut_url
    ):
        m_add_project.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_strings_based_project(**in_params) == "response"
        m_add_project.assert_called_once_with(request_data=request_data)

    @mock.patch("crowdin_api.api_resources.projects.resource.ProjectsResource.add_project")
    def test_add_file_based_project_new_fields(self, m_add_project, base_absolut_url):
        m_add_project.return_value = "response"

        new_fields = {
            "tagsDetection": ProjectTagsDetection.SKIP_TAGS,
            "taskBasedAccessControl": True,
            "publicDownloads": True,
            "hiddenStringsProofreadersAccess": False,
            "useGlobalTm": True,
            "showTmSuggestionsDialects": True,
            "qaCheckIsActive": True,
            "qaCheckCategories": QACheckCategories(empty=True, unifiedPlaceholders=False),
            "qaChecksIgnorableCategories": QAChecksIgnorableCategories(numbers=True),
            "languageMapping": {"uk": {"locale": "uk-UA"}},
            "glossaryAccessOption": ProjectGlossaryAccessOption.MANAGE_DRAFTS,
            "tmPreTranslate": {
                "enabled": True,
                "autoApproveOption": TmPreTranslateAutoApproveOption.ALL,
                "minimumMatchRatio": TmPreTranslateMinimumMatchRatio.PERFECT,
            },
            "mtPreTranslate": {"enabled": True, "mts": [{"mtId": 1, "languageIds": ["uk"]}]},
            "aiPreTranslate": {"enabled": True, "aiPrompts": [{"aiPromptId": 2, "languageIds": ["uk"]}]},
            "editorSuggestionAiPromptId": 3,
            "qaCheckActionAiPromptId": 4,
            "contextReviewAiPromptId": 5,
            "savingsReportSettingsTemplateId": 6,
            "assignedStyleGuides": [7, 8],
            "inContext": True,
            "inContextProcessHiddenStrings": True,
            "inContextPseudoLanguageId": "ach",
            "tmContextType": ProjectTmContextType.PREV_AND_NEXT_SEGMENT,
            "groupId": 9,
            "templateId": 10,
            "steps": [{"id": 1, "languages": ["uk"], "config": {"assignees": {"uk": [1]}}}],
            "vendorId": 11,
            "mtEngineId": 12,
            "taskReviewerIds": [13],
            "delayedWorkflowStart": True,
            "exportWithMinApprovalsCount": 1,
            "exportStringsThatPassedWorkflow": False,
            "qaApprovalsCount": 2,
            "customQaCheckIds": [14],
            "externalQaCheckIds": [15],
            "fields": {"some-field": "value"},
            "alignmentActionAiPromptId": 16,
        }

        resource = self.get_resource(base_absolut_url)
        assert resource.add_file_based_project(
            name="name", sourceLanguageId="en", **new_fields
        ) == "response"

        expected = {key: None for key in ADD_FILE_BASED_PROJECT_BASE_FIELDS}
        expected.update(FILE_BASED_NEW_FIELDS)
        expected.update({"name": "name", "sourceLanguageId": "en"})
        expected.update(new_fields)
        m_add_project.assert_called_once_with(request_data=expected)

    @mock.patch("crowdin_api.api_resources.projects.resource.ProjectsResource.add_project")
    def test_add_strings_based_project_new_fields(self, m_add_project, base_absolut_url):
        m_add_project.return_value = "response"

        new_fields = {
            "tagsDetection": ProjectTagsDetection.AUTO,
            "taskBasedAccessControl": True,
            "showTmSuggestionsDialects": False,
            "normalizePlaceholder": True,
            "glossaryAccessOption": ProjectGlossaryAccessOption.READ_ONLY,
            "tmPreTranslate": {"enabled": False},
            "mtPreTranslate": {"enabled": False},
            "aiPreTranslate": {"enabled": False},
            "editorSuggestionAiPromptId": 1,
            "qaCheckActionAiPromptId": 2,
            "contextReviewAiPromptId": 3,
            "savingsReportSettingsTemplateId": 4,
            "assignedStyleGuides": [5],
            "inContext": False,
            "groupId": 6,
            "templateId": 7,
            "steps": [{"id": 1, "mtId": 2}],
            "vendorId": 8,
            "mtEngineId": 9,
            "taskReviewerIds": [10],
            "delayedWorkflowStart": False,
            "exportWithMinApprovalsCount": 0,
            "exportStringsThatPassedWorkflow": True,
            "qaApprovalsCount": 1,
            "customQaCheckIds": [11],
            "externalQaCheckIds": [12],
            "fields": {"some-field": 1},
            "alignmentActionAiPromptId": 13,
        }

        resource = self.get_resource(base_absolut_url)
        assert resource.add_strings_based_project(
            name="name", sourceLanguageId="en", **new_fields
        ) == "response"

        expected = {key: None for key in ADD_STRINGS_BASED_PROJECT_BASE_FIELDS}
        expected.update(STRINGS_BASED_NEW_FIELDS)
        expected.update({"name": "name", "sourceLanguageId": "en"})
        expected.update(new_fields)
        m_add_project.assert_called_once_with(request_data=expected)

    @pytest.mark.parametrize(
        "method_name, deprecated_params",
        (
            ("add_file_based_project", {"glossaryAccess": True}),
            ("add_file_based_project", {"preTranslationAiPromptId": 1}),
            ("add_strings_based_project", {"glossaryAccess": False}),
            ("add_strings_based_project", {"preTranslationAiPromptId": 1}),
        ),
    )
    @mock.patch("crowdin_api.api_resources.projects.resource.ProjectsResource.add_project")
    def test_add_project_deprecated_params(
        self, m_add_project, method_name, deprecated_params, base_absolut_url
    ):
        m_add_project.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        with pytest.warns(DeprecationWarning):
            assert getattr(resource, method_name)(
                name="name", sourceLanguageId="en", **deprecated_params
            ) == "response"

        request_data = m_add_project.call_args.kwargs["request_data"]
        for key, value in deprecated_params.items():
            assert request_data[key] == value

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_project(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_project(projectId=1) == "response"
        m_request.assert_called_once_with(method="get", path="projects/1")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_project(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_project(projectId=1) == "response"
        m_request.assert_called_once_with(method="delete", path="projects/1")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_project(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": ProjectPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_project(projectId=1, data=data) == "response"
        m_request.assert_called_once_with(method="patch", request_data=data, path="projects/1")

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/file-format-settings"),
            ({"projectId": 1, "fileFormatSettingsId": 2}, "projects/1/file-format-settings/2"),
        ),
    )
    def test_get_project_file_format_settings_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_project_file_format_settings_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_project_file_custom_segmentation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_project_file_custom_segmentation(
            projectId=1,
            fileFormatSettingsId=2
        ) == "response"

        m_request.assert_called_once_with(
            method="get",
            path="projects/1/file-format-settings/2/custom-segmentations",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_reset_project_file_custom_segmentation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.reset_project_file_custom_segmentation(
            projectId=1,
            fileFormatSettingsId=2
        ) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path="projects/1/file-format-settings/2/custom-segmentations",
        )

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "offset": 0,
                    "limit": 10,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_project_file_format_settings(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_project_file_format_settings(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_project_file_format_settings_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "format": "properties",
                    "settings": {
                        "escapeQuotes": 1,
                        "exportPattern": "string"
                    }
                },
                {
                    "format": "properties",
                    "settings": {
                        "escapeQuotes": 1,
                        "exportPattern": "string"
                    }
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_project_file_format_settings(self, m_add_project, in_params, request_data, base_absolut_url):
        m_add_project.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_project_file_format_settings(projectId=1, **in_params) == "response"
        m_add_project.assert_called_once_with(
            method="post",
            path=resource.get_project_file_format_settings_path(projectId=1),
            request_data=request_data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_project_file_format_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_project_file_format_settings(projectId=1, fileFormatSettingsId=2) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=resource.get_project_file_format_settings_path(projectId=1, fileFormatSettingsId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_project_file_format_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_project_file_format_settings(projectId=1, fileFormatSettingsId=2) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_project_file_format_settings_path(projectId=1, fileFormatSettingsId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_project_file_format_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {"value": "test", "op": PatchOperation.REPLACE, "path": ProjectFilePatchPath.FORMAT}
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_project_file_format_settings(
            projectId=1, fileFormatSettingsId=2, data=data
        ) == "response"

        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_project_file_format_settings_path(projectId=1, fileFormatSettingsId=2),
        )

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/strings-exporter-settings"),
            ({"projectId": 1, "systemStringExporterSettingsId": 2}, "projects/1/strings-exporter-settings/2"),
        ),
    )
    def test_get_strings_exporter_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_strings_exporter_path(**in_params) == path

    @mock.patch("crowdin_api.api_resources.abstract.resources.BaseResource._get_entire_data")
    def test_list_project_strings_exporter_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_project_strings_exporter_settings(1) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_strings_exporter_path(1)
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "format": "android",
                    "settings": {
                        "convertPlaceholders": True,
                    },
                },
                {
                    "format": "android",
                    "settings": {
                        "convertPlaceholders": True,
                    },
                },
            ),
            (
                {
                    "format": "macosx",
                    "settings": {
                        "convertPlaceholders": True,
                    },
                },
                {
                    "format": "macosx",
                    "settings": {
                        "convertPlaceholders": True,
                    },
                },
            ),
            (
                {
                    "format": "xliff",
                    "settings": {
                        "languagePaitMapping": {
                            "uk": "es",
                            "de": "en",
                        },
                    },
                },
                {
                    "format": "xliff",
                    "settings": {
                        "languagePaitMapping": {
                            "uk": "es",
                            "de": "en",
                        },
                    },
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_project_strings_exporter_settings(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_project_strings_exporter_settings(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_strings_exporter_path(projectId=1),
            request_data=request_data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_project_strings_exporter_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_project_strings_exporter_settings(
            projectId=1, systemStringExporterSettingsId=2
        ) == "response"

        m_request.assert_called_once_with(
            method="get",
            path=resource.get_strings_exporter_path(
                projectId=1, systemStringExporterSettingsId=2
            ),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_project_strings_exporter_settings(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_project_strings_exporter_settings(
            projectId=1, systemStringExporterSettingsId=2
        ) == "response"

        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_strings_exporter_path(
                projectId=1, systemStringExporterSettingsId=2
            ),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "format": "android",
                    "settings": {
                        "convertPlaceholders": True,
                        "useCdataForStringsWithTags": True,
                    },
                },
                [
                    {"op": "replace", "path": "/format", "value": "android"},
                    {
                        "op": "replace",
                        "path": "/settings",
                        "value": {
                            "convertPlaceholders": True,
                            "useCdataForStringsWithTags": True,
                        },
                    },
                ],
            ),
            (
                {"format": "macosx"},
                [{"op": "replace", "path": "/format", "value": "macosx"}],
            ),
            (
                {"settings": {"copySourceToEmptyTarget": True}},
                [
                    {
                        "op": "replace",
                        "path": "/settings",
                        "value": {"copySourceToEmptyTarget": True},
                    }
                ],
            ),
            (
                {
                    "data": [
                        {
                            "op": PatchOperation.REPLACE,
                            "path": StringsExporterSettingsPatchPath.SETTINGS,
                            "value": {"exportContext": True},
                        }
                    ]
                },
                [
                    {
                        "op": PatchOperation.REPLACE,
                        "path": StringsExporterSettingsPatchPath.SETTINGS,
                        "value": {"exportContext": True},
                    }
                ],
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_project_strings_exporter_settings(
        self, m_request, in_params, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_project_strings_exporter_settings(
            projectId=1,
            systemStringExporterSettingsId=2,
            **in_params,
        ) == "response"

        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_strings_exporter_path(projectId=1, systemStringExporterSettingsId=2),
            request_data=request_data,
        )
