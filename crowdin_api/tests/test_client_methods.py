import pytest

from crowdin_api import CrowdinClient
from crowdin_api.exceptions import CrowdinException


def test_groups_without_organization():
    client = CrowdinClient()

    with pytest.raises(CrowdinException, match="Not implemented for the base API"):
        client.groups.list_groups()


def test_teams_without_organization():
    client = CrowdinClient()

    with pytest.raises(CrowdinException, match="Not implemented for the base API"):
        client.teams.list_teams()


def test_workflows_without_organization():
    client = CrowdinClient()

    with pytest.raises(CrowdinException, match="Not implemented for the base API"):
        client.workflows.list_workflow_templates()
