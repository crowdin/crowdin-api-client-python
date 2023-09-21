import abc
from datetime import datetime
from typing import Dict, Iterable, Optional
from deprecated import deprecated

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.reports.enums import (
    ContributionMode,
    Currency,
    Format,
    GroupBy,
    Unit,
    ReportLabelIncludeType,
)
from crowdin_api.api_resources.reports.requests.cost_estimation_post_editing import (
    IndividualRate as CostEstimationPeIndividualRate,
    NetRateSchemes as CostEstimationPeNetRateSchemes
)
from crowdin_api.api_resources.reports.requests.translation_costs_post_editing import (
    IndividualRate as TranslationCostsPeIndividualRate,
    NetRateSchemes as TranslationCostsPeNetRateSchemes
)
from crowdin_api.api_resources.reports.types import (
    FuzzyIndividualRate,
    FuzzyRegularRate,
    SimpleIndividualRate,
    SimpleRegularRate,
    StepTypes,
    ReportSettingsTemplatesPatchRequest,
    Config,
    BaseRates
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
    @deprecated("Use other methods instead")
    def generate_simple_cost_estimate_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    @deprecated("Use other methods instead")
    def generate_fuzzy_cost_estimate_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    @deprecated("Use other methods instead")
    def generate_simple_translation_cost_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    @deprecated("Use other methods instead")
    def generate_fuzzy_translation_cost_report(self, projectId: int, **kwargs):
        raise NotImplementedError("Not implemented")

    def generate_top_members_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        languageId: Optional[str] = None,
        format: Optional[Format] = Format.XLSX,
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

    def generate_costs_estimation_post_editing_general_report(
        self,
        project_id: int,
        base_rates: BaseRates,
        individual_rates: Iterable[CostEstimationPeIndividualRate],
        net_rate_schemes: CostEstimationPeNetRateSchemes,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        calculate_internal_matches: Optional[bool] = None,
        include_pre_translated_strings: Optional[bool] = None,
        language_id: Optional[str] = None,
        file_ids: Optional[Iterable[int]] = None,
        directory_ids: Optional[Iterable[int]] = None,
        branch_ids: Optional[Iterable[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        label_ids: Optional[Iterable[int]] = None,
        label_include_type: Optional[ReportLabelIncludeType] = None
    ):
        """
        Generate Report.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "costs-estimation-pe",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "calculateInternalMatches": calculate_internal_matches,
                    "includePreTranslatedStrings": include_pre_translated_strings,
                    "languageId": language_id,
                    "fileIds": file_ids,
                    "directoryIds": directory_ids,
                    "branchIds": branch_ids,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "labelIds": label_ids,
                    "labelIncludeType": label_include_type
                }
            }
        )

    def generate_costs_estimation_post_editing_by_task_report(
        self,
        project_id: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        base_rates: Optional[BaseRates] = None,
        individual_rates: Optional[Iterable[CostEstimationPeIndividualRate]] = None,
        net_rate_schemes: Optional[CostEstimationPeNetRateSchemes] = None,
        calculate_internal_matches: Optional[bool] = None,
        include_pre_translated_strings: Optional[bool] = None,
        task_id: Optional[int] = None
    ):
        """
        Generate Report.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "costs-estimation-pe",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "calculateInternalMatches": calculate_internal_matches,
                    "includePreTranslatedStrings": include_pre_translated_strings,
                    "taskId": task_id
                }
            }
        )

    def generate_translation_costs_post_editing_general_report(
        self,
        project_id: int,
        base_rates: BaseRates,
        individual_rates: Iterable[CostEstimationPeIndividualRate],
        net_rate_schemes: CostEstimationPeNetRateSchemes,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        group_by: Optional[GroupBy] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        language_id: Optional[str] = None,
        user_ids: Optional[Iterable[int]] = None,
        file_ids: Optional[Iterable[int]] = None,
        directory_ids: Optional[Iterable[int]] = None,
        branch_ids: Optional[Iterable[int]] = None
    ):
        """
        Generate Report.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "translation-costs-pe",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "groupBy": group_by,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "languageId": language_id,
                    "userIds": user_ids,
                    "fileIds": file_ids,
                    "directoryIds": directory_ids,
                    "branchIds": branch_ids
                }
            }
        )

    def generate_translation_costs_post_editing_by_task_report(
        self,
        project_id: int,
        base_rates: BaseRates,
        individual_rates: Iterable[CostEstimationPeIndividualRate],
        net_rate_schemes: CostEstimationPeNetRateSchemes,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        task_id: Optional[int] = None
    ):
        """
        Generate Report.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.projects.reports.post
        """

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "translation-costs-pe",
                "schema": {
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "taskId": task_id
                }
            }
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

        return self._get_entire_data(
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

    @deprecated("Use other methods instead")
    def generate_simple_cost_estimate_report(
        self,
        projectId: int,
        # Schema
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        languageId: Optional[str] = None,
        fileIds: Optional[Iterable[int]] = None,
        format: Optional[Format] = Format.XLSX,
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

    @deprecated("Use other methods instead")
    def generate_fuzzy_cost_estimate_report(
        self,
        projectId: int,
        # Schema
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        languageId: Optional[str] = None,
        fileIds: Optional[Iterable[int]] = None,
        format: Optional[Format] = Format.XLSX,
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

    @deprecated("Use other methods instead")
    def generate_simple_translation_cost_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = Format.XLSX,
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

    @deprecated("Use other methods instead")
    def generate_fuzzy_translation_cost_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = Format.XLSX,
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

    @deprecated("Use other methods instead")
    def generate_simple_cost_estimate_report(
        self,
        projectId: int,
        # Schema
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        languageId: Optional[str] = None,
        fileIds: Optional[Iterable[int]] = None,
        format: Optional[Format] = Format.XLSX,
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

    @deprecated("Use other methods instead")
    def generate_fuzzy_cost_estimate_report(
        self,
        projectId: int,
        # Schema
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        languageId: Optional[str] = None,
        fileIds: Optional[Iterable[int]] = None,
        format: Optional[Format] = Format.XLSX,
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

    @deprecated("Use other methods instead")
    def generate_simple_translation_cost_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = Format.XLSX,
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

    @deprecated("Use other methods instead")
    def generate_fuzzy_translation_cost_report(
        self,
        projectId: int,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = Format.XLSX,
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

    @staticmethod
    def get_group_reports_path(group_id: int, report_id: Optional[str] = None):
        if report_id is not None:
            return f"groups/{group_id}/reports/{group_id}"

        return f"groups/{group_id}/reports"

    def generate_group_report(self, group_id: int, request_data: Dict):
        """
        Generate Group Report.

        Link to documentation for enterprise:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.requester.request(
            method="post",
            path=self.get_group_reports_path(group_id=group_id),
            request_data=request_data,
        )

    def generate_group_translation_costs_post_editing_general_report(
        self,
        group_id: int,
        base_rates: BaseRates,
        individual_rates: Iterable[TranslationCostsPeIndividualRate],
        net_rate_schemes: TranslationCostsPeNetRateSchemes,
        project_ids: Optional[Iterable[int]] = None,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        group_by: Optional[GroupBy] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        user_ids: Optional[Iterable[int]] = None
    ):
        """
        Generate Group Report (General).

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-translation-costs-pe",
                "schema": {
                    "projectIds": project_ids,
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "groupBy": group_by,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids
                },
            },
        )

    @staticmethod
    def get_organization_reports_path(report_id: Optional[str] = None):
        if report_id is not None:
            return f"reports/{report_id}"

        return "reports"

    def generate_organization_translation_costs_post_editing_general_report(
        self,
        base_rates: BaseRates,
        individual_rates: Iterable[TranslationCostsPeIndividualRate],
        net_rate_schemes: TranslationCostsPeNetRateSchemes,
        project_ids: Optional[Iterable[int]] = None,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        group_by: Optional[GroupBy] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        user_ids: Optional[Iterable[int]] = None
    ):
        """
        Generate Organization Report (General).

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.reports.post
        """

        return self.requester.request(
            method="post",
            path=self.get_organization_reports_path(),
            request_data={
                "name": "group-translation-costs-pe",
                "schema": {
                    "projectIds": project_ids,
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "groupBy": group_by,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids
                },
            },
        )
