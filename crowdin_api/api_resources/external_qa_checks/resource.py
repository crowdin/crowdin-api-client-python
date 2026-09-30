from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource


class ExternalQaChecksResource(BaseResource):
    """
    Resource for External QA Checks.

    Crowdin Enterprise only.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/External-QA-Checks
    """

    def get_external_qa_checks_path(self, externalQaCheckId: Optional[int] = None):
        if externalQaCheckId is not None:
            return f"external-qa-checks/{externalQaCheckId}"

        return "external-qa-checks"

    def list_external_qa_checks(
        self,
        projectId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List External QA Checks.

        :param projectId: Filter External QA Checks by Project Identifier

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.external-qa-checks.getMany
        """
        params = {"projectId": projectId}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_external_qa_checks_path(),
            params=params,
        )

    def get_external_qa_check(self, externalQaCheckId: int):
        """
        Get External QA Check.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.external-qa-checks.get
        """
        return self.requester.request(
            method="get",
            path=self.get_external_qa_checks_path(externalQaCheckId=externalQaCheckId),
        )
