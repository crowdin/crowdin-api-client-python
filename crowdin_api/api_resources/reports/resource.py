from datetime import datetime
from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.reports.enums import (
    ContributionMode,
    Currency,
    Format,
    GroupBy,
    Unit,
)
from crowdin_api.api_resources.reports.types import (
    FuzzyIndividualRate,
    FuzzyRegularRate,
    SimpleIndividualRate,
    SimpleRegularRate,
)


class ReportsResource(BaseResource):
    """
    Resource for Reports.

    Reports help to estimate costs, calculate translation costs, and identify the top members.

    Use API to generate Cost Estimate, Translation Cost, and Top Members reports. You can then
    export reports in .xlsx or .csv file formats. Report generation is an asynchronous operation
    and shall be completed with a sequence of API methods.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Reports
    """

    def get_reports_path(self, projectId: int, reportId: Optional[str] = None):
        if reportId is not None:
            return f"projects/{projectId}/reports/{reportId}"

        return f"projects/{projectId}/reports"

    def generate_report(self, projectId: int, request_data: Dict):
        """
        Generate Report.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.post
        """

        return self.requester.request(
            method="post",
            path=self.get_reports_path(projectId=projectId),
            request_data=request_data,
        )

    def generate_simple_cost_estimate_report(
        self,
        projectId: int,
        # Schema
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        languageId: Optional[str] = None,
        fileIds: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        regularRates: Optional[Iterable[SimpleRegularRate]] = None,
        individualRates: Optional[Iterable[SimpleIndividualRate]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Cost Estimate Schema).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "costs-estimation",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "mode": "simple",
                    "languageId": languageId,
                    "fileIds": fileIds,
                    "format": format,
                    "regularRates": regularRates,
                    "individualRates": individualRates,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                },
            },
        )

    def generate_fuzzy_cost_estimate_report(
        self,
        projectId: int,
        # Schema
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        languageId: Optional[str] = None,
        fileIds: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        calculateInternalFuzzyMatches: Optional[bool] = None,
        regularRates: Optional[Iterable[FuzzyRegularRate]] = None,
        individualRates: Optional[Iterable[FuzzyIndividualRate]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Cost Estimate Fuzzy Mode).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "costs-estimation",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "mode": "fuzzy",
                    "languageId": languageId,
                    "fileIds": fileIds,
                    "format": format,
                    "calculateInternalFuzzyMatches": calculateInternalFuzzyMatches,
                    "regularRates": regularRates,
                    "individualRates": individualRates,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                },
            },
        )

    def generate_simple_translation_cost_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        groupBy: Optional[GroupBy] = None,
        regularRates: Optional[Iterable[SimpleRegularRate]] = None,
        individualRates: Optional[Iterable[SimpleIndividualRate]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Translation Cost).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "translation-costs",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "mode": "simple",
                    "format": format,
                    "groupBy": groupBy,
                    "regularRates": regularRates,
                    "individualRates": individualRates,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                },
            },
        )

    def generate_fuzzy_translation_cost_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        groupBy: Optional[GroupBy] = None,
        regularRates: Optional[Iterable[FuzzyRegularRate]] = None,
        individualRates: Optional[Iterable[FuzzyIndividualRate]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Translation Fuzzy Cost).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "translation-costs",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "mode": "fuzzy",
                    "format": format,
                    "groupBy": groupBy,
                    "regularRates": regularRates,
                    "individualRates": individualRates,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                },
            },
        )

    def generate_top_members_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        languageId: Optional[str] = None,
        format: Optional[Format] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Top Members).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "top-members",
                "schema": {
                    "unit": unit,
                    "languageId": languageId,
                    "format": format,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                },
            },
        )

    def generate_contribution_raw_data_report(
        self,
        projectId: int,
        mode: ContributionMode,
        unit: Optional[Unit] = None,
        languageId: Optional[str] = None,
        userId: Optional[int] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Contribution Raw Data).

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "contribution-raw-data",
                "schema": {
                    "mode": mode,
                    "unit": unit,
                    "languageId": languageId,
                    "userId": userId,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                },
            },
        )

    def check_report_generation_status(self, projectId: int, reportId: str):
        """
        Check Report Generation Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_reports_path(projectId=projectId, reportId=reportId),
        )

    def download_report(self, projectId: int, reportId: str):
        """
        Download Report.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.projects.reports.download.download
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_reports_path(projectId=projectId, reportId=reportId)}/download",
        )
