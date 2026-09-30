from datetime import datetime
from typing import Any, Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.advisors.enums import (
    AdvisorInsightOutcome,
    AdvisorInsightStatus,
)
from crowdin_api.api_resources.advisors.types import (
    AdvisorCheckInspector,
    AdvisorInsightMetric,
    AdvisorInsightPatchRequest,
    AdvisorInsightRecommendation,
)
from crowdin_api.utils import convert_to_query_list


class AdvisorsResource(BaseResource):
    """
    Resource for Advisors.

    Advisors run inspectors against a project and report insights about its localization health.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Advisors

    Link to documentation for enterprise:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Advisors
    """

    def get_advisor_checks_path(self, projectId: int, checkId: Optional[str] = None):
        if checkId is not None:
            return f"projects/{projectId}/advisors/checks/{checkId}"
        return f"projects/{projectId}/advisors/checks"

    def get_advisor_insights_path(self, projectId: int, insightId: Optional[int] = None):
        if insightId is not None:
            return f"projects/{projectId}/advisors/insights/{insightId}"
        return f"projects/{projectId}/advisors/insights"

    def create_advisor_check(
        self,
        category: Optional[str] = None,
        inspectors: Optional[Iterable[AdvisorCheckInspector]] = None,
        projectId: Optional[int] = None,
    ):
        """
        Create Advisor Check.

        At most one of `category` or `inspectors` may be set; if neither is set, every
        inspector is re-checked.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.advisors.checks.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.advisors.checks.post
        """
        if category is not None and inspectors is not None:
            raise ValueError("You can set only one of category or inspectors.")

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_advisor_checks_path(projectId=projectId),
            request_data={"category": category, "inspectors": inspectors},
        )

    def get_advisor_check_status(self, checkId: str, projectId: Optional[int] = None):
        """
        Get Advisor Check Status.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.advisors.checks.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.advisors.checks.get
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_advisor_checks_path(projectId=projectId, checkId=checkId),
        )

    def list_advisor_insights(
        self,
        projectId: Optional[int] = None,
        isDismissed: Optional[bool] = None,
        status: Optional[
            Union[str, AdvisorInsightStatus, Iterable[Union[str, AdvisorInsightStatus]]]
        ] = None,
        outcome: Optional[
            Union[str, AdvisorInsightOutcome, Iterable[Union[str, AdvisorInsightOutcome]]]
        ] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Advisor Insights.

        `status` and `outcome` accept a single value or a list of values (sent comma-separated).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.advisors.insights.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.advisors.insights.getMany
        """
        projectId = projectId or self.get_project_id()
        params = {
            "isDismissed": isDismissed,
            "status": convert_to_query_list(status),
            "outcome": convert_to_query_list(outcome),
        }
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_advisor_insights_path(projectId=projectId),
            params=params,
        )

    def edit_advisor_insight(
        self,
        insightId: int,
        data: Iterable[AdvisorInsightPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Advisor Insight.

        Currently only `/isDismissed` is patchable.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.advisors.insights.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.advisors.insights.patch
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="patch",
            path=self.get_advisor_insights_path(projectId=projectId, insightId=insightId),
            request_data=data,
        )

    def create_or_update_application_advisor_insight(
        self,
        applicationIdentifier: str,
        moduleKey: str,
        outcome: AdvisorInsightOutcome,
        checkedAt: Optional[Union[datetime, str]] = None,
        metrics: Optional[Iterable[AdvisorInsightMetric]] = None,
        recommendations: Optional[Iterable[AdvisorInsightRecommendation]] = None,
        payload: Optional[Dict[str, Any]] = None,
        projectId: Optional[int] = None,
    ):
        """
        Create or Update Application Advisor Insight.

        Called by an installed application's `advisor-inspector` module to publish its check result.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.applications.modules.advisors.insights.put

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.applications.modules.advisors.insights.put
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="put",
            path=(
                f"projects/{projectId}/applications/{applicationIdentifier}"
                f"/modules/{moduleKey}/advisors/insights"
            ),
            request_data={
                "outcome": outcome,
                "checkedAt": checkedAt,
                "metrics": metrics,
                "recommendations": recommendations,
                "payload": payload,
            },
        )
