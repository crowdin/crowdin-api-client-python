from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.source_files.enums import (
    BranchPatchPath,
    DirectoryPatchPath,
    FilePatchPath,
    FileType,
    Priority,
)
from crowdin_api.api_resources.source_files.resource import SourceFilesResource
from crowdin_api.requester import APIRequester


class TestSourceFilesResource:
    resource_class = SourceFilesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    # Branches
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/branches"),
            ({"projectId": 1, "branchId": 2}, "projects/1/branches/2"),
        ),
    )
    def test_get_branch_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_branch_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {"offset": 0, "limit": 10, "name": None},
            ),
            (
                {"offset": 0, "limit": 10, "name": "test"},
                {"offset": 0, "limit": 10, "name": "test"},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_project_branches(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_project_branches(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_branch_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "name": "name",
                    "title": "title",
                },
                {
                    "name": "name",
                    "title": "title",
                    "exportPattern": None,
                    "priority": None,
                },
            ),
            (
                {
                    "name": "name",
                    "title": "title",
                    "exportPattern": "exportPattern",
                    "priority": Priority.LOW,
                },
                {
                    "name": "name",
                    "title": "title",
                    "exportPattern": "exportPattern",
                    "priority": Priority.LOW,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_branch(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_branch(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_branch_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_branch(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_branch(projectId=1, branchId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_branch_path(projectId=1, branchId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_branch(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_branch(projectId=1, branchId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_branch_path(projectId=1, branchId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_branch(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": BranchPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_branch(projectId=1, branchId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_branch_path(projectId=1, branchId=2),
        )

    # Directories
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/directories"),
            ({"projectId": 1, "directoryId": 2}, "projects/1/directories/2"),
        ),
    )
    def test_get_directory_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_directory_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {
                    "offset": 0,
                    "limit": 10,
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "branchId": None,
                    "directoryId": None,
                    "filter": None,
                    "recursion": None,
                },
            ),
            (
                {
                    "offset": 0,
                    "limit": 10,
                    "branchId": 1,
                    "directoryId": 2,
                    "filter": "filter",
                    "recursion": "recursion",
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "branchId": 1,
                    "directoryId": 2,
                    "filter": "filter",
                    "recursion": "recursion",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_directories(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_directories(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_directory_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "name": "name",
                },
                {
                    "name": "name",
                    "branchId": None,
                    "directoryId": None,
                    "title": None,
                    "exportPattern": None,
                    "priority": None,
                },
            ),
            (
                {
                    "name": "name",
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "exportPattern": "exportPattern",
                    "priority": Priority.LOW,
                },
                {
                    "name": "name",
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "exportPattern": "exportPattern",
                    "priority": Priority.LOW,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_directory(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_directory(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_directory_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_directory(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_directory(projectId=1, directoryId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_directory_path(projectId=1, directoryId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_directory(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_directory(projectId=1, directoryId=2) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_directory_path(projectId=1, directoryId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_directory(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": DirectoryPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_directory(projectId=1, directoryId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_directory_path(projectId=1, directoryId=2),
        )

    # Files
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/files"),
            ({"projectId": 1, "fileId": 2}, "projects/1/files/2"),
        ),
    )
    def test_get_file_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_file_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "offset": 0,
                    "limit": 10,
                    "branchId": None,
                    "directoryId": None,
                    "filter": None,
                    "recursion": None,
                },
            ),
            (
                {
                    "offset": 0,
                    "limit": 10,
                    "branchId": 1,
                    "directoryId": 1,
                    "filter": "filter",
                    "recursion": "recursion",
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "branchId": 1,
                    "directoryId": 1,
                    "filter": "filter",
                    "recursion": "recursion",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_files(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_files(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_file_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "name": "name",
                    "storageId": 1,
                },
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": None,
                    "directoryId": None,
                    "title": None,
                    "type": FileType.AUTO,
                    "importOptions": None,
                    "exportOptions": None,
                    "excludedTargetLanguages": None,
                    "attachLabelIds": None,
                },
            ),
            (
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.RESW,
                    "importOptions": {"contentSegmentation": True},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.RESW,
                    "importOptions": {"contentSegmentation": True},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
            ),
            (
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.HTML,
                    "importOptions": {"excludedElements": ["element"]},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.HTML,
                    "importOptions": {"excludedElements": ["element"]},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
            ),
            (
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.HTML,
                    "importOptions": {"excludedFrontMatterElements": ["element"]},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.HTML,
                    "importOptions": {"excludedFrontMatterElements": ["element"]},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
            ),
            (
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.MD,
                    "importOptions": {"excludeCodeBlocks": False},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
                {
                    "name": "name",
                    "storageId": 1,
                    "branchId": 1,
                    "directoryId": 1,
                    "title": "title",
                    "type": FileType.MD,
                    "importOptions": {"excludeCodeBlocks": False},
                    "exportOptions": {"exportPattern": "exportPattern"},
                    "excludedTargetLanguages": ["excludedTargetLanguages"],
                    "attachLabelIds": [1],
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_file(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_file(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_file_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_file(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_file(projectId=1, fileId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_file_path(projectId=1, fileId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_file(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_file(projectId=1, fileId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_file_path(projectId=1, fileId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_file(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [{"value": "test", "op": PatchOperation.REPLACE, "path": FilePatchPath.NAME}]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_file(projectId=1, fileId=2, data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_file_path(projectId=1, fileId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_update_file(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.update_file(projectId=1, fileId=2, storageId=1) == "response"
        m_request.assert_called_once_with(
            method="put",
            request_data={
                "storageId": 1,
                "updateOption": None,
                "importOptions": None,
                "exportOptions": None,
                "attachLabelIds": None,
                "detachLabelIds": None,
            },
            path=resource.get_file_path(projectId=1, fileId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_restore_file(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.restore_file(projectId=1, fileId=2, revisionId=3) == "response"
        m_request.assert_called_once_with(
            method="put",
            request_data={"revisionId": 3},
            path=resource.get_file_path(projectId=1, fileId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_file_preview(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_file_preview(1, 1) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_file_path(1, 1) + "/preview",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_file(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_file(projectId=1, fileId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_file_path(projectId=1, fileId=2) + "/download",
        )

    # File Revisions
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1, "fileId": 2}, "projects/1/files/2/revisions"),
            (
                {"projectId": 1, "fileId": 2, "revisionId": 3},
                "projects/1/files/2/revisions/3",
            ),
        ),
    )
    def test_get_file_revisions_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_file_revisions_path(**in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_file_revisions(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_file_revisions(projectId=1, fileId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=resource.get_page_params(None, None, None),
            path=resource.get_file_revisions_path(projectId=1, fileId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_file_revision(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_file_revision(projectId=1, fileId=2, revisionId=3)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_file_revisions_path(projectId=1, fileId=2, revisionId=3),
        )
