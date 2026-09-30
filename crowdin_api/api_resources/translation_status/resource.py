import warnings
from typing import Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.translation_status.enums import (
    Category,
    QaChecksRevalidationCategory,
    Validation,
)
from crowdin_api.api_resources.translation_status.types import ValidateQaChecksRequest


class TranslationStatusResource(BaseResource):
    """
    Resource for Translation Status.

    Status represents the general localization progress on both translations and proofreading.

    Use API to check translation and proofreading progress on different levels:
    file, language, branch, directory.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Translation-Status
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.branches.languages.progress.getMany
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.directories.languages.progress.getMany
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.files.languages.progress.getMany
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.languages.files.progress.getMany
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.languages.progress.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {"languageIds": None if languageIds is None else ",".join(languageIds)}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/languages/progress",
            params=params,
        )

    def get_qa_checks_revalidation_path(self, projectId: int, revalidationId: Optional[str] = None):
        if revalidationId is not None:
            return f"projects/{projectId}/qa-checks/revalidate/{revalidationId}"

        warnings.warn(
            "Calling QA checks revalidation status/cancel without `revalidationId` is deprecated, "
            "pass the `revalidationId` returned by `start_qa_checks_revalidation`",
            DeprecationWarning,
            stacklevel=3,
        )
        return f"projects/{projectId}/qa-checks/revalidate"

    def start_qa_checks_revalidation(
        self,
        projectId: Optional[int] = None,
        qaCheckCategories: Optional[Iterable[QaChecksRevalidationCategory]] = None,
        languageIds: Optional[Iterable[str]] = None,
        failedOnly: Optional[bool] = None,
        externalQaCheckIds: Optional[Iterable[int]] = None,
    ):
        """
        Start QA Checks Revalidation.

        Triggers a new QA checks revalidation job for the project.

        `externalQaCheckIds` is available in Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translation-Status/operation/api.projects.qa-checks.revalidate.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#tag/Translation-Status/operation/api.projects.qa-checks.revalidate.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/qa-checks/revalidate",
            request_data={
                "qaCheckCategories": qaCheckCategories,
                "languageIds": languageIds,
                "failedOnly": failedOnly,
                "externalQaCheckIds": externalQaCheckIds,
            },
        )

    def get_qa_checks_revalidation_status(
        self,
        projectId: Optional[int] = None,
        revalidationId: Optional[str] = None,
    ):
        """
        Get QA Checks Revalidation Status.

        Returns the status of the QA checks revalidation job identified by `revalidationId`
        (the identifier returned by `start_qa_checks_revalidation`). Omitting `revalidationId`
        is deprecated.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translation-Status/operation/api.projects.qa-checks.revalidate.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_qa_checks_revalidation_path(
                projectId=projectId, revalidationId=revalidationId
            ),
        )

    def cancel_qa_checks_revalidation(
        self,
        projectId: Optional[int] = None,
        revalidationId: Optional[str] = None,
    ):
        """
        Cancel QA Checks Revalidation.

        Cancels the QA checks revalidation job identified by `revalidationId`
        (the identifier returned by `start_qa_checks_revalidation`). Omitting `revalidationId`
        is deprecated.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#tag/Translation-Status/operation/api.projects.qa-checks.revalidate.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_qa_checks_revalidation_path(
                projectId=projectId, revalidationId=revalidationId
            ),
        )

    def validate_text_by_qa_checks(
        self,
        data: Iterable[ValidateQaChecksRequest],
        projectId: Optional[int] = None,
    ):
        """
        Validate Text by QA Checks.

        Runs QA checks against the passed texts without saving them as translations.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.translations.validate-qa-checks.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.translations.validate-qa-checks.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/translations/validate-qa-checks",
            request_data=data,
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
        taskId: Optional[int] = None,
        fileId: Optional[int] = None,
        branchId: Optional[int] = None,
    ):
        """
        List QA Check Issues.

        `fileId` is available in file-based projects only, `branchId` in string-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.qa-checks.getMany
        """

        projectId = projectId or self.get_project_id()
        params = {
            "languageIds": None if languageIds is None else ",".join(languageIds),
            "category": ",".join((item.value for item in category)) if category else None,
            "validation": ",".join((item.value for item in validation)) if validation else None,
            "taskId": taskId,
            "fileId": fileId,
            "branchId": branchId,
        }
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=f"projects/{projectId}/qa-checks",
            params=params,
        )
