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
                    "hasManagerAccess": HasManagerAccess.FALSE,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_projects(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_projects(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path="projects",
        )

    @pytest.mark.parametrize(
        "in_params, post_data",
        (
            (
                {
                    "name": "Some",
                    "sourceLanguageId": 1,
                },
                {
                    "name": "Some",
                    "sourceLanguageId": 1,
                    "identifier": None,
                    "type": ProjectType.FILE_BASED,
                    "normalizePlaceholder": None,
                    "saveMetaInfoInSource": None,
                    "targetLanguageIds": None,
                    "visibility": ProjectVisibility.PRIVATE,
                    "languageAccessPolicy": ProjectLanguageAccessPolicy.OPEN,
                    "cname": None,
                    "description": None,
                    "skipUntranslatedStrings": None,
                    "skipUntranslatedFiles": None,
                    "exportApprovedOnly": None,
                },
            ),
            (
                {
                    "name": "Some",
                    "sourceLanguageId": 1,
                    "identifier": "Some",
                    "type": ProjectType.STRING_BASED,
                    "normalizePlaceholder": True,
                    "saveMetaInfoInSource": False,
                    "targetLanguageIds": ["sm"],
                    "visibility": ProjectVisibility.OPEN,
                    "languageAccessPolicy": ProjectLanguageAccessPolicy.MODERATE,
                    "cname": "None",
                    "description": "None",
                    "skipUntranslatedStrings": True,
                    "skipUntranslatedFiles": True,
                    "exportApprovedOnly": True,
                },
                {
                    "name": "Some",
                    "sourceLanguageId": 1,
                    "identifier": "Some",
                    "type": ProjectType.STRING_BASED,
                    "normalizePlaceholder": True,
                    "saveMetaInfoInSource": False,
                    "targetLanguageIds": ["sm"],
                    "visibility": ProjectVisibility.OPEN,
                    "languageAccessPolicy": ProjectLanguageAccessPolicy.MODERATE,
                    "cname": "None",
                    "description": "None",
                    "skipUntranslatedStrings": True,
                    "skipUntranslatedFiles": True,
                    "exportApprovedOnly": True,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_project(self, m_request, in_params, post_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_project(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post", path="projects", post_data=post_data
        )

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
        m_request.assert_called_once_with(
            method="patch", post_data=data, path="projects/1"
        )
