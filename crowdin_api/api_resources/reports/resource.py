import abc
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
    StepTypes,
    ReportSettingsTemplatesPatchRequest,
    Config,
)


class BaseReportsResource(BaseResource):
    def get_reports_path(self, projectId: int, reportId: Optional[str] = None):
        if reportId is not None:
            return f"projects/{projectId}/reports/{reportId}"

        return f"projects/{projectId}/reports"

    def generate_report(self, projectId: int, request_data: Dict):
        """
        Generate Report.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.reports.download.download
        """

        return self.requester.request(
            method="post",
            path=self.get_reports_path(projectId=projectId),
            request_data=request_data,
        )

    @abc.abstractmethod
    def generate_simple_cost_estimate_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    def generate_fuzzy_cost_estimate_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    def generate_simple_translation_cost_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    def generate_fuzzy_translation_cost_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

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
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.get

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_reports_path(projectId=projectId, reportId=reportId),
        )

    def download_report(self, projectId: int, reportId: str):
        """
        Download Report.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.download.download

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.download.download
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_reports_path(projectId=projectId, reportId=reportId)}/download",
        )


class BaseReportSettingsTemplatesResource(BaseResource):
    def get_report_settings_templates_path(
        self,
        projectId: int,
        reportSettingsTemplateId: Optional[int] = None
    ):
        if reportSettingsTemplateId is not None:
            return f"projects/{projectId}/reports/settings-templates/{reportSettingsTemplateId}"

        return f"projects/{projectId}/reports/settings-templates"

    def list_report_settings_template(
        self,
        projectId: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        List Report Settings Templates.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.settings-templates.getMany

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.settings-templates.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_report_settings_templates_path(projectId=projectId),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def add_report_settings_template(
        self,
        projectId: int,
        name: str,
        currency: Currency,
        unit: Unit,
        config: Config,
    ):
        """
        Add Report Settings Templates.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.settings-templates.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.settings-templates.post
        """

        return self.requester.request(
            method="post",
            path=self.get_report_settings_templates_path(
                projectId=projectId,
            ),
            request_data={
                "name": name,
                "currency": currency,
                "unit": unit,
                "mode": "simple",
                "config": config
            }
        )

    def get_report_settings_template(
        self,
        projectId: int,
        reportSettingsTemplateId: int,
    ):
        """
        Get Report Settings Templates.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.settings-templates.get

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.settings-templates.get
        """

        return self.requester.request(
            method="get",
            path=self.get_report_settings_templates_path(
                projectId=projectId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )

    def edit_report_settings_template(
        self,
        projectId: int,
        reportSettingsTemplateId: int,
        data: Iterable[ReportSettingsTemplatesPatchRequest]

    ):
        """
        Edit Report Settings Templates.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.settings-templates.patch

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.settings-templates.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_report_settings_templates_path(
                projectId=projectId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
            request_data=data,
        )

    def delete_report_settings_template(
        self,
        projectId: int,
        reportSettingsTemplateId: int,
    ):
        """
        Delete Report Settings Templates.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.settings-templates.delete

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.settings-templates.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_report_settings_templates_path(
                projectId=projectId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )


class ReportsResource(BaseReportsResource, BaseReportSettingsTemplatesResource):
    """
    Resource for Reports.

    Reports help to estimate costs, calculate translation costs, and identify the top members.

    Use API to generate Cost Estimate, Translation Cost, and Top Members reports. You can then
    export reports in .xlsx or .csv file formats. Report generation is an asynchronous operation
    and shall be completed with a sequence of API methods.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Reports
    """

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
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post
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
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post
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


class EnterpriseReportsResource(BaseReportsResource, BaseReportSettingsTemplatesResource):
    """
    Resource for Enterprise Reports.

    Reports help to estimate costs, calculate translation costs, and identify the top members.

    Use API to generate Cost Estimate, Translation Cost, and Top Members reports. You can then
    export reports in .xlsx or .csv file formats. Report generation is an asynchronous operation
    and shall be completed with a sequence of API methods.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Reports
    """
    @staticmethod
    def _prepare_stepTypes(step_types_const: dict, stepTypes: Optional[Iterable[StepTypes]] = None):
        if isinstance(stepTypes, list):
            stepTypes = [
                {**item, **step_types_const}
                for item in stepTypes if isinstance(item, dict)
            ]

        return stepTypes

    def generate_simple_cost_estimate_report(
        self,
        projectId: int,
        # Schema
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        languageId: Optional[str] = None,
        fileIds: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        stepTypes: Optional[Iterable[StepTypes]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Cost Estimate schema).

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post
        """
        step_types_const = {
            "type": "Translate",
            "mode": "simple",
        }
        stepTypes = self._prepare_stepTypes(step_types_const=step_types_const, stepTypes=stepTypes)

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "costs-estimation",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "languageId": languageId,
                    "fileIds": fileIds,
                    "format": format,
                    "stepTypes": stepTypes,
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
        stepTypes: Optional[Iterable[StepTypes]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Cost Estimate Fuzzy Mode).

        Links to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
        """
        step_types_const = {
            "type": "Translate",
            "mode": "fuzzy",
            "calculateInternalFuzzyMatches": False,
        }
        stepTypes = self._prepare_stepTypes(step_types_const=step_types_const, stepTypes=stepTypes)

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "costs-estimation",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "stepTypes": stepTypes,
                    "languageId": languageId,
                    "fileIds": fileIds,
                    "format": format,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                }
            }
        )

    def generate_simple_translation_cost_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        groupBy: Optional[GroupBy] = None,
        stepTypes: Optional[Iterable[StepTypes]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Translation Cost).

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
        """
        step_types_const = {
            "type": "Translate",
            "mode": "simple",
        }
        stepTypes = self._prepare_stepTypes(step_types_const=step_types_const, stepTypes=stepTypes)

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "translation-costs",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "stepTypes": stepTypes,
                    "format": format,
                    "groupBy": groupBy,
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
        stepTypes: Optional[Iterable[StepTypes]] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        Generate Report(Translation Cost Fuzzy Mode).

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
        """
        step_types_const = {
            "type": "Translate",
            "mode": "fuzzy",
        }
        stepTypes = self._prepare_stepTypes(step_types_const=step_types_const, stepTypes=stepTypes)

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "translation-costs",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "stepTypes": stepTypes,
                    "format": format,
                    "groupBy": groupBy,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                },
            },
        )
