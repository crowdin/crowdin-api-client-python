from unittest import mock

import pytest
from crowdin_api.api_resources import ProjectsResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import (
    HasManagerAccess,
    ProjectLanguageAccessPolicy,
    ProjectPatchPath,
    ProjectType,
    ProjectVisibility,
)
from crowdin_api.requester import APIRequester


class TestProjectsResource:
    resource_class = ProjectsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "offset": 0,
                    "limit": 10,
                    "userId": 1,
                    "hasManagerAccess": HasManagerAccess.TRUE,
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "userId": 1,
                    "hasManagerAccess": HasManagerAccess.TRUE,
                },
            ),
            (
                {"offset": 0, "limit": 10},
                {
                    "offset": 0,
                    "limit": 10,
                    "userId": None,
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
