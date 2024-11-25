from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.translation_status.enums import Category, Validation


class TranslationStatusResource(BaseResource):
    """
    Resource for Translation Status.

    Status represents the general localization progress on both translations and proofreading.

    Use API to check translation and proofreading progress on different levels:
    file, language, branch, directory.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Translation-Status
    """

    def get_branch_progress(
        self,
        branchId: int,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Get Branch Progress.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.branches.languages.progress.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/branches/{branchId}/languages/progress",
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def get_directory_progress(
        self,
        directoryId: int,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Get Directory Progress.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.directories.languages.progress.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/directories/{directoryId}/languages/progress",
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def get_file_progress(
        self,
        fileId: int,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Get File Progress.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.files.languages.progress.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/files/{fileId}/languages/progress",
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def get_language_progress(
        self,
        languageId: str,
        projectId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Get Language Progress.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.languages.files.progress.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/languages/{languageId}/progress",
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def get_project_progress(
        self,
        projectId: Optional[int] = None,
        languageIds: Optional[Iterable[str]] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        Get Project Progress.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.languages.progress.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"languageIds": None if languageIds is None else ",".join(languageIds)}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/languages/progress",
            params=params,
        )

    def list_qa_check_issues(
        self,
        projectId: Optional[int] = None,
        category: Optional[Iterable[Category]] = None,
        validation: Optional[Iterable[Validation]] = None,
        languageIds: Optional[Iterable[str]] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List QA Check Issues.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.qa-checks.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "languageIds": None if languageIds is None else ",".join(languageIds),
            "category": ",".join((item.value for item in category)) if category else None,
            "validation": ",".join((item.value for item in validation)) if validation else None,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/qa-checks",
            params=params,
        )
