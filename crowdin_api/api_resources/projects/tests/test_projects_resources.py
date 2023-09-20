from unittest import mock

import pytest
from crowdin_api.api_resources import ProjectsResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import (
    HasManagerAccess,
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


class TestProjectsResource:
    resource_class = ProjectsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

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
                    "offset": 0,
                    "limit": 10,
                    "userId": 1,
                    "groupId": 1,
                    "hasManagerAccess": HasManagerAccess.TRUE,
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "userId": 1,
                    "groupId": 1,
                    "hasManagerAccess": HasManagerAccess.TRUE,
                },
            ),
            (
                {"offset": 0, "limit": 10},
                {
                    "offset": 0,
                    "limit": 10,
                    "userId": None,
                    "groupId": None,
                    "hasManagerAccess": None,
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
                },
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
                        EMPTY=True,
                        SIZE=True,
                        TAGS=True,
                        SPACES=True,
                        VARIABLES=True,
                        PUNCTUATION=True,
                        SYMBOLREGISTER=True,
                        SPECIALSYMBOLS=True,
                        WRONGTRANSLATION=True,
                        SPELLCHECK=True,
                        ICU=True,
                        TERMS=True,
                        DUPLICATE=True,
                    ),
                    "qaChecksIgnorableCategories": QAChecksIgnorableCategories(
                        EMPTY=True,
                        SIZE=True,
                        TAGS=True,
                        SPACES=True,
                        VARIABLES=True,
                        PUNCTUATION=True,
                        SYMBOLREGISTER=True,
                        SPECIALSYMBOLS=True,
                        WRONGTRANSLATION=True,
                        SPELLCHECK=True,
                        ICU=True,
                        TERMS=True,
                        DUPLICATE=True,
                        FTL=True,
                        ANDROID=True
                    ),
                    "languageMapping": {},
                    "glossaryAccess": True,
                    "notificationSettings": NotificationSettings(
                        translatorNewStrings=True,
                        managerNewStrings=True,
                        managerLanguageCompleted=True,
                    ),
                },
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
                        EMPTY=True,
                        SIZE=True,
                        TAGS=True,
                        SPACES=True,
                        VARIABLES=True,
                        PUNCTUATION=True,
                        SYMBOLREGISTER=True,
                        SPECIALSYMBOLS=True,
                        WRONGTRANSLATION=True,
                        SPELLCHECK=True,
                        ICU=True,
                        TERMS=True,
                        DUPLICATE=True,
                    ),
                    "qaChecksIgnorableCategories": QAChecksIgnorableCategories(
                        EMPTY=True,
                        SIZE=True,
                        TAGS=True,
                        SPACES=True,
                        VARIABLES=True,
                        PUNCTUATION=True,
                        SYMBOLREGISTER=True,
                        SPECIALSYMBOLS=True,
                        WRONGTRANSLATION=True,
                        SPELLCHECK=True,
                        ICU=True,
                        TERMS=True,
                        DUPLICATE=True,
                        FTL=True,
                        ANDROID=True,
                    ),
                    "languageMapping": {},
                    "glossaryAccess": True,
                    "notificationSettings": NotificationSettings(
                        translatorNewStrings=True,
                        managerNewStrings=True,
                        managerLanguageCompleted=True,
                    ),
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
    def test_edit_project_strings_exporter_settings(self, m_request, in_params, request_data, base_absolut_url):
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
