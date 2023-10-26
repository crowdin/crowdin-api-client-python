from unittest import mock

import pytest

from crowdin_api.api_resources import TeamsResource
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.teams.enums import TeamPatchPath
from crowdin_api.requester import APIRequester


class TestTeamsResources:
    resource_class = TeamsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({}, "teams"),
            ({"teamId": 1}, "teams/1"),
        ),
    )
    def test_get_teams_path(self, incoming_data, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_teams_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"teamId": 1}, "teams/1/members"),
            ({"teamId": 1, "memberId": 2}, "teams/1/members/2"),
        ),
    )
    def test_get_members_path(self, incoming_data, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_members_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {"teamId": 1},
                {
                    "teamId": 1,
                    "accessToAllWorkflowSteps": True,
                    "managerAccess": False,
                    "permissions": None,
                    "roles": None,
                }
            ),
            (
                {
                    "teamId": 1,
                    "accessToAllWorkflowSteps": False,
                    "managerAccess": True,
                    "permissions": {
                        "it": {
                            "workflowStepIds": [313]
                        },
                        "de": {"workflowStepIds": "all"}
                    }
                },
                {
                    "teamId": 1,
                    "accessToAllWorkflowSteps": False,
                    "managerAccess": True,
                    "permissions": {
                        "it": {
                            "workflowStepIds": [313]
                        },
                        "de": {"workflowStepIds": "all"}
                    },
                    "roles": None
                },
            ),
            (
                {
                    "teamId": 1,
                    "accessToAllWorkflowSteps": False,
                    "managerAccess": False,
                    "permissions": {
                        "it": {
                            "workflowStepIds": [
                                313
                            ]
                        },
                        "de": {
                            "workflowStepIds": "all"
                        }
                    },
                    "roles": [
                        {
                            "name": "translator",
                            "permissions": {
                                "allLanguages": False,
                                "languagesAccess": {
                                    "uk": {
                                        "allContent": False,
                                        "workflowStepIds": [
                                            882
                                        ]
                                    },
                                    "it": {
                                        "allContent": True
                                    }
                                }
                            }
                        },
                        {
                            "name": "proofreader",
                            "permissions": {
                                "allLanguages": True,
                                "languagesAccess": []
                            }
                        }
                    ]
                },
                {
                    "teamId": 1,
                    "accessToAllWorkflowSteps": False,
                    "managerAccess": False,
                    "permissions": {
                        "it": {
                            "workflowStepIds": [
                                313
                            ]
                        },
                        "de": {
                            "workflowStepIds": "all"
                        }
                    },
                    "roles": [
                        {
                            "name": "translator",
                            "permissions": {
                                "allLanguages": False,
                                "languagesAccess": {
                                    "uk": {
                                        "allContent": False,
                                        "workflowStepIds": [
                                            882
                                        ]
                                    },
                                    "it": {
                                        "allContent": True
                                    }
                                }
                            }
                        },
                        {
                            "name": "proofreader",
                            "permissions": {
                                "allLanguages": True,
                                "languagesAccess": []
                            }
                        }
                    ]
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_team_to_project(self, m_request, incoming_data, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_team_to_project(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/teams",
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_teams(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_teams(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_teams_path(),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_team(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_team(name="test") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_teams_path(),
            request_data={"name": "test"},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_team(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_team(teamId=1) == "response"
        m_request.assert_called_once_with(method="get", path=resource.get_teams_path(teamId=1))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_team(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_team(teamId=1) == "response"
        m_request.assert_called_once_with(method="delete", path=resource.get_teams_path(teamId=1))

    @pytest.mark.parametrize(
        "value",
        [
            "test",
            True,
            False,
            [1, 2, 3],
            [{}, {}]
        ]
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_team(self, m_request, base_absolut_url, value):
        m_request.return_value = "response"

        data = [
            {
                "value": value,
                "op": PatchOperation.REPLACE,
                "path": TeamPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_team(teamId=1, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_teams_path(teamId=1),
        )

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_teams_member_list(self, m_request, incoming_data, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.teams_member_list(teamId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_members_path(teamId=1),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_team_members(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_team_members(teamId=1, userIds=[1, 2, 3]) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_members_path(teamId=1),
            request_data={"userIds": [1, 2, 3]},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_all_team_members(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_all_team_members(teamId=1) == "response"
        m_request.assert_called_once_with(method="delete", path=resource.get_members_path(teamId=1))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_team_member(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_team_member(teamId=1, memberId=2) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_members_path(teamId=1, memberId=2)
        )
