import abc
from datetime import datetime
from typing import Dict, Iterable, Optional, Union
from deprecated import deprecated

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.reports.enums import (
    ExportFormat,
    ScopeType,
    ContributionMode,
    Currency,
    Format,
    GroupBy,
    Unit,
    ReportLabelIncludeType,
    SavingActivityMode,
    EditorIssueType,
    TaskType,
    TaskUsageReportType,
    TaskUsageStatus,
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
    BaseRates,
    HourlyBaseRates,
    HourlyIndividualRate,
    PostEditingConfig,
    HourlyConfig,
)


class BaseReportsResource(BaseResource):
    def get_reports_path(self, projectId: int, reportId: Optional[str] = None):
        if reportId is not None:
            return f"projects/{projectId}/reports/{reportId}"

        return f"projects/{projectId}/reports"

    def generate_report(self, request_data: Dict, projectId: Optional[int] = None):
        """
        Generate Report.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_reports_path(projectId=projectId),
            request_data=request_data,
        )

    @abc.abstractmethod
    @deprecated("Use other methods instead")
    def generate_simple_cost_estimate_report(
        self, projectId: Optional[int] = None, **kwargs
    ):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    @deprecated("Use other methods instead")
    def generate_fuzzy_cost_estimate_report(
        self, projectId: Optional[int] = None, **kwargs
    ):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    @deprecated("Use other methods instead")
    def generate_simple_translation_cost_report(
        self, projectId: Optional[int] = None, **kwargs
    ):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    @deprecated("Use other methods instead")
    def generate_fuzzy_translation_cost_report(
        self, projectId: Optional[int] = None, **kwargs
    ):
        raise NotImplementedError("Not implemented")

    def generate_top_members_report(
        self,
        projectId: Optional[int] = None,
        unit: Optional[Unit] = None,
        languageId: Optional[str] = None,
        format: Optional[Format] = Format.XLSX,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        userIds: Optional[Iterable[int]] = None,
    ):
        """
        Generate Report(Top Members).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

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
                    "userIds": userIds,
                },
            },
        )

    def generate_contribution_raw_data_report(
        self,
        mode: ContributionMode,
        projectId: Optional[int] = None,
        unit: Optional[Unit] = None,
        languageId: Optional[str] = None,
        userId: Optional[int] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        columns: Optional[Iterable[str]] = None,
        tmIds: Optional[Iterable[int]] = None,
        mtIds: Optional[Iterable[int]] = None,
        aiPromptIds: Optional[Iterable[int]] = None,
        fileIds: Optional[Iterable[int]] = None,
        directoryIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
    ):
        """
        Generate Report(Contribution Raw Data).

        `fileIds` and `directoryIds` are available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

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
                    "columns": columns,
                    "tmIds": tmIds,
                    "mtIds": mtIds,
                    "aiPromptIds": aiPromptIds,
                    "fileIds": fileIds,
                    "directoryIds": directoryIds,
                    "branchIds": branchIds,
                },
            },
        )

    def generate_contribution_raw_data_by_task_report(
        self,
        mode: ContributionMode,
        task_id: int,
        project_id: Optional[int] = None,
        unit: Optional[Unit] = None,
        columns: Optional[Iterable[str]] = None,
        tm_ids: Optional[Iterable[int]] = None,
        mt_ids: Optional[Iterable[int]] = None,
        ai_prompt_ids: Optional[Iterable[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """
        Generate Report(Contribution Raw Data By Task).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "contribution-raw-data",
                "schema": {
                    "mode": mode,
                    "unit": unit,
                    "taskId": task_id,
                    "columns": columns,
                    "tmIds": tm_ids,
                    "mtIds": mt_ids,
                    "aiPromptIds": ai_prompt_ids,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_source_content_updates_report(
        self,
        project_id: Optional[int] = None,
        unit: Optional[Unit] = None,
        format: Optional[Format] = Format.XLSX,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """
        Generate Report(Source Content Updates).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "source-content-updates",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_project_members_report(
        self,
        project_id: Optional[int] = None,
        format: Optional[Format] = Format.XLSX,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """
        Generate Report(Project Members).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "project-members",
                "schema": {
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_editor_issues_report(
        self,
        project_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        format: Optional[Format] = Format.XLSX,
        issue_type: Optional[Union[EditorIssueType, str]] = None,
    ):
        """
        Generate Report(Editor Issues).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "editor-issues",
                "schema": {
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "format": format,
                    "issueType": issue_type
                },
            },
        )

    def generate_qa_check_issues_report(
        self,
        project_id: Optional[int] = None,
        format: Optional[Format] = Format.XLSX,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        language_id: Optional[str] = None,
    ):
        """
        Generate Report(Qa Check Issues).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "qa-check-issues",
                "schema": {
                    "format": format,
                    "languageId": language_id,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_saving_activity_report(
        self,
        project_id: Optional[int] = None,
        unit: Optional[Unit] = None,
        language_id: Optional[str] = None,
        format: Optional[Format] = Format.XLSX,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        mode: Optional[SavingActivityMode] = None,
        file_ids: Optional[Iterable[int]] = None,
        directory_ids: Optional[Iterable[int]] = None,
        branch_ids: Optional[Iterable[int]] = None,
        user_ids: Optional[Iterable[int]] = None,
    ):
        """
        Generate Report(Saving Activity).

        `file_ids` and `directory_ids` are available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "saving-activity",
                "schema": {
                    "unit": unit,
                    "languageId": language_id,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "mode": mode,
                    "fileIds": file_ids,
                    "directoryIds": directory_ids,
                    "branchIds": branch_ids,
                    "userIds": user_ids,
                },
            },
        )

    def generate_translation_activity_report(
        self,
        project_id: Optional[int] = None,
        unit: Optional[Unit] = None,
        language_id: Optional[str] = None,
        format: Optional[Format] = Format.XLSX,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        user_ids: Optional[Iterable[int]] = None,
    ):
        """
        Generate Report(Translation Activity).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "translation-activity",
                "schema": {
                    "unit": unit,
                    "languageId": language_id,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids,
                },
            },
        )

    def generate_pre_translate_accuracy_general_report(
        self,
        projectId: Optional[int] = None,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        postEditingCategories: Optional[Iterable[str]] = None,
        languageId: Optional[str] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
        matchScoreCategories: Optional[Iterable[str]] = None,
        fileIds: Optional[Iterable[int]] = None,
        directoryIds: Optional[Iterable[int]] = None,
        branchIds: Optional[Iterable[int]] = None,
        labelIds: Optional[Iterable[int]] = None,
        labelIncludeType: Optional[ReportLabelIncludeType] = None,
        skipArchiving: Optional[bool] = None,
    ):
        """
        Generate Report(Pre-Translate Accuracy General).

        `postEditingCategories` is deprecated by the API, use `matchScoreCategories` instead.

        `fileIds` and `directoryIds` are available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "pre-translate-accuracy",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "postEditingCategories": postEditingCategories,
                    "matchScoreCategories": matchScoreCategories,
                    "languageId": languageId,
                    "dateFrom": dateFrom,
                    "dateTo": dateTo,
                    "fileIds": fileIds,
                    "directoryIds": directoryIds,
                    "branchIds": branchIds,
                    "labelIds": labelIds,
                    "labelIncludeType": labelIncludeType,
                    "skipArchiving": skipArchiving,
                },
            },
        )

    def generate_pre_translate_accuracy_by_task_report(
        self,
        projectId: Optional[int] = None,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        postEditingCategories: Optional[Iterable[str]] = None,
        taskId: Optional[int] = None,
        matchScoreCategories: Optional[Iterable[str]] = None,
        skipArchiving: Optional[bool] = None,
    ):
        """
        Generate Report(Pre-Translate Accuracy By Task).

        `postEditingCategories` is deprecated by the API, use `matchScoreCategories` instead.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

        return self.generate_report(
            projectId=projectId,
            request_data={
                "name": "pre-translate-accuracy",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "postEditingCategories": postEditingCategories,
                    "matchScoreCategories": matchScoreCategories,
                    "taskId": taskId,
                    "skipArchiving": skipArchiving,
                },
            },
        )

    def generate_translator_accuracy_report(
        self,
        project_id: Optional[int] = None,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        match_score_categories: Optional[Iterable[str]] = None,
        language_id: Optional[str] = None,
        user_ids: Optional[Iterable[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        file_ids: Optional[Iterable[int]] = None,
        directory_ids: Optional[Iterable[int]] = None,
        branch_ids: Optional[Iterable[int]] = None,
        label_ids: Optional[Iterable[int]] = None,
        label_include_type: Optional[ReportLabelIncludeType] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Report(Translator Accuracy).

        `file_ids` and `directory_ids` are available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "translator-accuracy",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "matchScoreCategories": match_score_categories,
                    "languageId": language_id,
                    "userIds": user_ids,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "fileIds": file_ids,
                    "directoryIds": directory_ids,
                    "branchIds": branch_ids,
                    "labelIds": label_ids,
                    "labelIncludeType": label_include_type,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_costs_estimation_post_editing_general_report(
        self,
        base_rates: BaseRates,
        individual_rates: Iterable[CostEstimationPeIndividualRate],
        net_rate_schemes: CostEstimationPeNetRateSchemes,
        project_id: Optional[int] = None,
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
        label_include_type: Optional[ReportLabelIncludeType] = None,
        skip_archiving: Optional[bool] = None,
        workflow_step_id: Optional[int] = None,
    ):
        """
        Generate Report(Costs Estimation Post-Editing General).

        `workflow_step_id` is available for Crowdin Enterprise only.

        `file_ids` and `directory_ids` are available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

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
                    "labelIncludeType": label_include_type,
                    "skipArchiving": skip_archiving,
                    "workflowStepId": workflow_step_id,
                }
            }
        )

    def generate_costs_estimation_post_editing_by_task_report(
        self,
        project_id: Optional[int] = None,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        base_rates: Optional[BaseRates] = None,
        individual_rates: Optional[Iterable[CostEstimationPeIndividualRate]] = None,
        net_rate_schemes: Optional[CostEstimationPeNetRateSchemes] = None,
        calculate_internal_matches: Optional[bool] = None,
        include_pre_translated_strings: Optional[bool] = None,
        task_id: Optional[int] = None,
        task_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Report(Costs Estimation Post-Editing By Task).

        `task_id` is deprecated by the API, use `task_ids` instead.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

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
                    "taskId": task_id,
                    "taskIds": task_ids,
                    "skipArchiving": skip_archiving,
                }
            }
        )

    def generate_translation_costs_post_editing_general_report(
        self,
        base_rates: BaseRates,
        individual_rates: Iterable[CostEstimationPeIndividualRate],
        net_rate_schemes: CostEstimationPeNetRateSchemes,
        project_id: Optional[int] = None,
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
        branch_ids: Optional[Iterable[int]] = None,
        use_category_based_proofread_rates: Optional[bool] = None,
        use_tm_edit_distance: Optional[bool] = None,
        label_ids: Optional[Iterable[int]] = None,
        label_include_type: Optional[ReportLabelIncludeType] = None,
        skip_archiving: Optional[bool] = None,
        workflow_step_id: Optional[int] = None,
    ):
        """
        Generate Report(Translation Costs Post-Editing General).

        `workflow_step_id` is available for Crowdin Enterprise only.

        `file_ids` and `directory_ids` are available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

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
                    "branchIds": branch_ids,
                    "useCategoryBasedProofreadRates": use_category_based_proofread_rates,
                    "useTmEditDistance": use_tm_edit_distance,
                    "labelIds": label_ids,
                    "labelIncludeType": label_include_type,
                    "skipArchiving": skip_archiving,
                    "workflowStepId": workflow_step_id,
                }
            }
        )

    def generate_translation_costs_post_editing_by_task_report(
        self,
        base_rates: BaseRates,
        individual_rates: Iterable[CostEstimationPeIndividualRate],
        net_rate_schemes: CostEstimationPeNetRateSchemes,
        project_id: Optional[int] = None,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        task_id: Optional[int] = None,
        task_ids: Optional[Iterable[int]] = None,
        use_category_based_proofread_rates: Optional[bool] = None,
        use_tm_edit_distance: Optional[bool] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Report(Translation Costs Post-Editing By Task).

        `task_id` is deprecated by the API, use `task_ids` instead.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

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
                    "taskId": task_id,
                    "taskIds": task_ids,
                    "useCategoryBasedProofreadRates": use_category_based_proofread_rates,
                    "useTmEditDistance": use_tm_edit_distance,
                    "skipArchiving": skip_archiving,
                }
            }
        )

    def generate_time_spent_report(
        self,
        project_id: Optional[int] = None,
        format: Optional[Format] = None,
        group_by: Optional[GroupBy] = None,
        base_rates: Optional[HourlyBaseRates] = None,
        individual_rates: Optional[Iterable[HourlyIndividualRate]] = None,
        language_id: Optional[str] = None,
        user_ids: Optional[Iterable[int]] = None,
        type_tasks: Optional[TaskType] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        task_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
        workflow_step_id: Optional[int] = None,
    ):
        """
        Generate Report(Time Spent).

        `workflow_step_id` is available for Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "time-spent",
                "schema": {
                    "format": format,
                    "groupBy": group_by,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "languageId": language_id,
                    "userIds": user_ids,
                    "typeTasks": type_tasks,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "taskIds": task_ids,
                    "workflowStepId": workflow_step_id,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def check_report_generation_status(
        self, reportId: str, projectId: Optional[int] = None
    ):
        """
        Check Report Generation Status.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_reports_path(projectId=projectId, reportId=reportId),
        )

    def download_report(self, reportId: str, projectId: Optional[int] = None):
        """
        Download Report.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.download.download

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.download.download
        """

        projectId = projectId or self.get_project_id()

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
        projectId: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        List Report Settings Templates.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.settings-templates.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.settings-templates.getMany
        """

        projectId = projectId or self.get_project_id()

        return self._get_entire_data(
            method="get",
            path=self.get_report_settings_templates_path(projectId=projectId),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def add_report_settings_template(
        self,
        name: str,
        currency: Currency,
        unit: Unit,
        config: Union[PostEditingConfig, HourlyConfig, Config],
        isPublic: Optional[bool] = None,
        projectId: Optional[int] = None,
        isGlobal: Optional[bool] = None,
    ):
        """
        Add Report Settings Templates.

        `isGlobal` is available for Crowdin only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.settings-templates.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.settings-templates.post
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_report_settings_templates_path(
                projectId=projectId,
            ),
            request_data={
                "name": name,
                "currency": currency,
                "unit": unit,
                "config": config,
                "isPublic": isPublic,
                "isGlobal": isGlobal,
            }
        )

    def get_report_settings_template(
        self,
        reportSettingsTemplateId: int,
        projectId: Optional[int] = None,
    ):
        """
        Get Report Settings Templates.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.settings-templates.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.settings-templates.get
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_report_settings_templates_path(
                projectId=projectId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )

    def edit_report_settings_template(
        self,
        reportSettingsTemplateId: int,
        data: Iterable[ReportSettingsTemplatesPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Report Settings Templates.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.settings-templates.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.settings-templates.patch
        """

        projectId = projectId or self.get_project_id()

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
        reportSettingsTemplateId: int,
        projectId: Optional[int] = None,
    ):
        """
        Delete Report Settings Templates.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.settings-templates.delete

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.settings-templates.delete
        """

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_report_settings_templates_path(
                projectId=projectId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )


class UserReportSettingsTemplatesResource(BaseReportSettingsTemplatesResource):
    """
    Resource for User Report Settings Templates API.

    Supporting the endpoints for managing user report settings templates.

    These methods are also available on `ReportsResource` and `EnterpriseReportsResource`
    (both platforms support `/users/{userId}/reports/settings-templates`).

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/User-Report-Settings-Templates
    """

    def get_user_report_settings_templates_path(
        self,
        userId: int,
        reportSettingsTemplateId: Optional[int] = None
    ):
        if reportSettingsTemplateId is not None:
            return f"users/{userId}/reports/settings-templates/{reportSettingsTemplateId}"

        return f"users/{userId}/reports/settings-templates"

    def list_user_report_settings_template(
        self,
        userId: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        List User Report Settings Templates.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.settings-templates.getMany
        """
        return self._get_entire_data(
            method="get",
            path=self.get_user_report_settings_templates_path(userId=userId),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def add_user_report_settings_template(
        self,
        userId: int,
        name: str,
        currency: Currency,
        unit: Unit,
        config: Union[PostEditingConfig, HourlyConfig, Config],
    ):
        """
        Add User Report Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.settings-templates.post
        """
        return self.requester.request(
            method="post",
            path=self.get_user_report_settings_templates_path(
                userId=userId,
            ),
            request_data={
                "name": name,
                "currency": currency,
                "unit": unit,
                "config": config,
            }
        )

    def get_user_report_settings_template(
        self,
        userId: int,
        reportSettingsTemplateId: int,
    ):
        """
        Get User Report Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.settings-templates.get
        """
        return self.requester.request(
            method="get",
            path=self.get_user_report_settings_templates_path(
                userId=userId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )

    def edit_user_report_settings_template(
        self,
        userId: int,
        reportSettingsTemplateId: int,
        data: Iterable[ReportSettingsTemplatesPatchRequest],
    ):
        """
        Edit User Report Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.settings-templates.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_user_report_settings_templates_path(
                userId=userId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
            request_data=data,
        )

    def delete_user_report_settings_template(
        self,
        userId: int,
        reportSettingsTemplateId: int,
    ):
        """
        Delete User Report Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.settings-templates.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_user_report_settings_templates_path(
                userId=userId,
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )


class ReportsResource(BaseReportsResource, UserReportSettingsTemplatesResource):
    """
    Resource for Reports.

    Reports help to estimate costs, calculate translation costs, and identify the top members.

    Use API to generate Cost Estimate, Translation Cost, and Top Members reports. You can then
    export reports in .xlsx or .csv file formats. Report generation is an asynchronous operation
    and shall be completed with a sequence of API methods.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Reports
    """

    def get_report_archive_path(self, userId: int, archiveId: Optional[int] = None):
        if archiveId is not None:
            return f"users/{userId}/reports/archives/{archiveId}"

        return f"users/{userId}/reports/archives"

    def get_report_archive_export_path(
        self,
        userId: int,
        archiveId: int,
        exportId: Optional[str] = None,
    ):
        if exportId is not None:
            return f"users/{userId}/reports/archives/{archiveId}/exports/{exportId}"

        return f"users/{userId}/reports/archives/{archiveId}/exports"

    def list_report_archives(
        self,
        userId: int,
        scopeType: Optional[str] = None,
        scopeId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        taskId: Optional[int] = None,
        name: Optional[str] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        List Report Archives

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.reports.archives.getMany
        """
        params = {
            "scopeType": scopeType,
            "scopeId": scopeId,
            "taskId": taskId,
            "name": name,
            "dateFrom": dateFrom,
            "dateTo": dateTo,
        }
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self._get_entire_data(
            method="get",
            path=self.get_report_archive_path(userId=userId),
            params=params,
        )

    def get_report_archive(self, userId: int, archiveId: int):
        """
        Get Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.archives.get
        """
        return self.requester.request(
            method="get",
            path=self.get_report_archive_path(userId=userId, archiveId=archiveId),
        )

    def delete_report_archive(self, userId: int, archiveId: int):
        """
        Delete Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.archives.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_report_archive_path(userId=userId, archiveId=archiveId),
        )

    def export_report_archive(
        self, userId: int, archiveId: int, format: Optional[ExportFormat] = None
    ):
        """
        Export Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.reports.archives.exports.post
        """
        format = format or ExportFormat.XLSX
        return self.requester.request(
            method="post",
            path=self.get_report_archive_export_path(
                userId=userId, archiveId=archiveId
            ),
            request_data={"format": format},
        )

    def check_report_archive_export_status(
        self, userId: int, archiveId: int, exportId: str
    ):
        """
        Check Report Archive Status

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.archives.exports.get
        """
        return self.requester.request(
            method="get",
            path=self.get_report_archive_export_path(
                userId=userId, archiveId=archiveId, exportId=exportId
            ),
        )

    def download_report_archive(
        self, userId: int, archiveId: int, exportId: str
    ):
        """
        Download Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.users.reports.archives.exports.download.get
        """
        path = str(
            self.get_report_archive_export_path(
                userId=userId, archiveId=archiveId, exportId=exportId
            )
            + "/download"
        )
        return self.requester.request(
            method="get",
            path=path,
        )

    @deprecated("Use other methods instead")
    def generate_simple_cost_estimate_report(
        self,
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

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
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

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
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

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
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post
        """

        projectId = projectId or self.get_project_id()

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


class EnterpriseReportsResource(BaseReportsResource, UserReportSettingsTemplatesResource):
    """
    Resource for Enterprise Reports.

    Reports help to estimate costs, calculate translation costs, and identify the top members.

    Use API to generate Cost Estimate, Translation Cost, and Top Members reports. You can then
    export reports in .xlsx or .csv file formats. Report generation is an asynchronous operation
    and shall be completed with a sequence of API methods.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Reports
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
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.reports.post
        """
        projectId = projectId or self.get_project_id()
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
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """
        projectId = projectId or self.get_project_id()
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
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """
        projectId = projectId or self.get_project_id()
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
        projectId: Optional[int] = None,
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
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """
        projectId = projectId or self.get_project_id()
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

    def get_report_archive_path(self, archiveId: Optional[int] = None):
        if archiveId is not None:
            return f"reports/archives/{archiveId}"

        return "reports/archives"

    def get_report_archive_export_path(
        self,
        archiveId: int,
        exportId: Optional[str] = None,
    ):
        if exportId is not None:
            return f"reports/archives/{archiveId}/exports/{exportId}"

        return f"reports/archives/{archiveId}/exports"

    def list_report_archives(
        self,
        scopeType: Optional[ScopeType] = None,
        scopeId: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        userId: Optional[int] = None,
        taskId: Optional[int] = None,
        name: Optional[str] = None,
        dateFrom: Optional[datetime] = None,
        dateTo: Optional[datetime] = None,
    ):
        """
        List Report Archives

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.archives.getMany
        """
        params = {
            "scopeType": scopeType,
            "scopeId": scopeId,
            "userId": userId,
            "taskId": taskId,
            "name": name,
            "dateFrom": dateFrom,
            "dateTo": dateTo,
        }
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self._get_entire_data(
            method="get",
            path=self.get_report_archive_path(),
            params=params,
        )

    def get_report_archive(self, archiveId: int):
        """
        Get Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.archives.get
        """
        return self.requester.request(
            method="get",
            path=self.get_report_archive_path(archiveId=archiveId),
        )

    def delete_report_archive(self, archiveId: int):
        """
        Delete Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.archives.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_report_archive_path(archiveId=archiveId),
        )

    def export_report_archive(
        self, archiveId: int, format: Optional[ExportFormat] = None
    ):
        """
        Export Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.archives.exports.post
        """
        format = format or ExportFormat.XLSX
        return self.requester.request(
            method="post",
            path=self.get_report_archive_export_path(archiveId=archiveId),
            request_data={"format": format},
        )

    def check_report_archive_export_status(self, archiveId: int, exportId: str):
        """
        Check Report Archive Status

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.archives.exports.get
        """
        return self.requester.request(
            method="get",
            path=self.get_report_archive_export_path(
                archiveId=archiveId, exportId=exportId
            ),
        )

    def download_report_archive(self, archiveId: int, exportId: str):
        """
        Download Report Archive

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.archives.exports.download.get
        """
        path = str(
            self.get_report_archive_export_path(archiveId=archiveId, exportId=exportId)
            + "/download"
        )
        return self.requester.request(
            method="get",
            path=path,
        )

    def generate_task_usage_report(
        self,
        project_id: Optional[int] = None,
        format: Optional[Format] = None,
        type: Optional[TaskUsageReportType] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        group_by: Optional[GroupBy] = None,
        type_tasks: Optional[TaskType] = None,
        language_id: Optional[str] = None,
        creator_id: Optional[int] = None,
        assignee_id: Optional[int] = None,
        words_count_from: Optional[int] = None,
        words_count_to: Optional[int] = None,
        statuses: Optional[Iterable[TaskUsageStatus]] = None,
    ):
        """
        Generate Report(Task Usage).

        `words_count_from` and `words_count_to` are used only with `time` type, `statuses` only
        with `cost` type.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.projects.reports.post
        """

        project_id = project_id or self.get_project_id()

        return self.generate_report(
            projectId=project_id,
            request_data={
                "name": "task-usage",
                "schema": {
                    "format": format,
                    "type": type,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "groupBy": group_by,
                    "typeTasks": type_tasks,
                    "languageId": language_id,
                    "creatorId": creator_id,
                    "assigneeId": assignee_id,
                    "wordsCountFrom": words_count_from,
                    "wordsCountTo": words_count_to,
                    "statuses": statuses,
                },
            },
        )

    # Project report settings templates are not available in Crowdin Enterprise API anymore
    @deprecated("Use `list_organization_report_settings_templates` instead")
    def list_report_settings_template(
        self,
        projectId: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        List Report Settings Templates.

        Deprecated: use `list_organization_report_settings_templates` instead.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.getMany
        """
        return super().list_report_settings_template(
            projectId=projectId, offset=offset, limit=limit
        )

    @deprecated("Use `add_organization_report_settings_template` instead")
    def add_report_settings_template(
        self,
        name: str,
        currency: Currency,
        unit: Unit,
        config: Union[PostEditingConfig, HourlyConfig, Config],
        isPublic: Optional[bool] = None,
        projectId: Optional[int] = None,
        isGlobal: Optional[bool] = None,
    ):
        """
        Add Report Settings Templates.

        Deprecated: use `add_organization_report_settings_template` instead.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.post
        """
        return super().add_report_settings_template(
            name=name,
            currency=currency,
            unit=unit,
            config=config,
            isPublic=isPublic,
            projectId=projectId,
            isGlobal=isGlobal,
        )

    @deprecated("Use `get_organization_report_settings_template` instead")
    def get_report_settings_template(
        self,
        reportSettingsTemplateId: int,
        projectId: Optional[int] = None,
    ):
        """
        Get Report Settings Templates.

        Deprecated: use `get_organization_report_settings_template` instead.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.get
        """
        return super().get_report_settings_template(
            reportSettingsTemplateId=reportSettingsTemplateId, projectId=projectId
        )

    @deprecated("Use `edit_organization_report_settings_template` instead")
    def edit_report_settings_template(
        self,
        reportSettingsTemplateId: int,
        data: Iterable[ReportSettingsTemplatesPatchRequest],
        projectId: Optional[int] = None,
    ):
        """
        Edit Report Settings Templates.

        Deprecated: use `edit_organization_report_settings_template` instead.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.patch
        """
        return super().edit_report_settings_template(
            reportSettingsTemplateId=reportSettingsTemplateId, data=data, projectId=projectId
        )

    @deprecated("Use `delete_organization_report_settings_template` instead")
    def delete_report_settings_template(
        self,
        reportSettingsTemplateId: int,
        projectId: Optional[int] = None,
    ):
        """
        Delete Report Settings Templates.

        Deprecated: use `delete_organization_report_settings_template` instead.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.delete
        """
        return super().delete_report_settings_template(
            reportSettingsTemplateId=reportSettingsTemplateId, projectId=projectId
        )

    @staticmethod
    def get_organization_report_settings_templates_path(
        reportSettingsTemplateId: Optional[int] = None,
    ):
        if reportSettingsTemplateId is not None:
            return f"reports/settings-templates/{reportSettingsTemplateId}"

        return "reports/settings-templates"

    def list_organization_report_settings_templates(
        self,
        project_id: Optional[int] = None,
        group_id: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Organization Report Settings Templates.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.getMany
        """
        params = {"projectId": project_id, "groupId": group_id}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_organization_report_settings_templates_path(),
            params=params,
        )

    def add_organization_report_settings_template(
        self,
        name: str,
        currency: Currency,
        unit: Unit,
        config: Union[PostEditingConfig, HourlyConfig],
        project_id: Optional[int] = None,
        group_id: Optional[int] = None,
        is_public: Optional[bool] = None,
    ):
        """
        Add Organization Report Settings Template.

        `project_id` and `group_id` can't be used together.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.post
        """
        return self.requester.request(
            method="post",
            path=self.get_organization_report_settings_templates_path(),
            request_data={
                "projectId": project_id,
                "groupId": group_id,
                "name": name,
                "currency": currency,
                "unit": unit,
                "config": config,
                "isPublic": is_public,
            },
        )

    def get_organization_report_settings_template(self, reportSettingsTemplateId: int):
        """
        Get Organization Report Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.get
        """
        return self.requester.request(
            method="get",
            path=self.get_organization_report_settings_templates_path(
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )

    def edit_organization_report_settings_template(
        self,
        reportSettingsTemplateId: int,
        data: Iterable[ReportSettingsTemplatesPatchRequest],
    ):
        """
        Edit Organization Report Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_organization_report_settings_templates_path(
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
            request_data=data,
        )

    def delete_organization_report_settings_template(self, reportSettingsTemplateId: int):
        """
        Delete Organization Report Settings Template.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.settings-templates.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_organization_report_settings_templates_path(
                reportSettingsTemplateId=reportSettingsTemplateId
            ),
        )

    @staticmethod
    def get_group_reports_path(group_id: int, report_id: Optional[str] = None):
        if report_id is not None:
            return f"groups/{group_id}/reports/{report_id}"

        return f"groups/{group_id}/reports"

    def generate_group_report(self, group_id: int, request_data: Dict):
        """
        Generate Group Report.

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.requester.request(
            method="post",
            path=self.get_group_reports_path(group_id=group_id),
            request_data=request_data,
        )

    def check_group_report_generation_status(self, group_id: int, report_id: str):
        """
        Check Group Report Generation Status.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_group_reports_path(group_id=group_id, report_id=report_id),
        )

    def download_group_report(self, group_id: int, report_id: str):
        """
        Download Group Report.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.download.download
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_group_reports_path(group_id=group_id, report_id=report_id)}/download",
        )

    @staticmethod
    def get_organization_reports_path(report_id: Optional[str] = None):
        if report_id is not None:
            return f"reports/{report_id}"

        return "reports"

    def generate_organization_report(self, request_data: Dict):
        """
        Generate Organization Report.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.requester.request(
            method="post",
            path=self.get_organization_reports_path(),
            request_data=request_data,
        )

    def check_organization_report_generation_status(self, report_id: str):
        """
        Check Organization Report Generation Status.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_organization_reports_path(report_id=report_id),
        )

    def download_organization_report(self, report_id: str):
        """
        Download Organization Report.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.download.download
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_organization_reports_path(report_id=report_id)}/download",
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
        user_ids: Optional[Iterable[int]] = None,
        use_category_based_proofread_rates: Optional[bool] = None,
        use_tm_edit_distance: Optional[bool] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Group Report (Translation Costs Post-Editing General).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-translation-costs-pe",
                "schema": {
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "projectIds": project_ids,
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "groupBy": group_by,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids,
                    "useCategoryBasedProofreadRates": use_category_based_proofread_rates,
                    "useTmEditDistance": use_tm_edit_distance,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_group_translation_costs_post_editing_by_task_report(
        self,
        group_id: int,
        base_rates: BaseRates,
        individual_rates: Iterable[TranslationCostsPeIndividualRate],
        net_rate_schemes: TranslationCostsPeNetRateSchemes,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        task_ids: Optional[Iterable[int]] = None,
        use_category_based_proofread_rates: Optional[bool] = None,
        use_tm_edit_distance: Optional[bool] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Group Report (Translation Costs Post-Editing By Task).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-translation-costs-pe",
                "schema": {
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "taskIds": task_ids,
                    "useCategoryBasedProofreadRates": use_category_based_proofread_rates,
                    "useTmEditDistance": use_tm_edit_distance,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_group_top_members_report(
        self,
        group_id: int,
        project_ids: Optional[Iterable[int]] = None,
        unit: Optional[Unit] = None,
        language_id: Optional[str] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        user_ids: Optional[Iterable[int]] = None,
    ):
        """
        Generate Group Report (Top Members).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-top-members",
                "schema": {
                    "projectIds": project_ids,
                    "unit": unit,
                    "languageId": language_id,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids,
                },
            },
        )

    def generate_group_task_usage_report(
        self,
        group_id: int,
        format: Optional[Format] = None,
        type: Optional[TaskUsageReportType] = None,
        project_ids: Optional[Iterable[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        group_by: Optional[GroupBy] = None,
        type_task: Optional[TaskType] = None,
        language_id: Optional[str] = None,
        creator_id: Optional[int] = None,
        assignee_id: Optional[int] = None,
        words_count_from: Optional[int] = None,
        words_count_to: Optional[int] = None,
        statuses: Optional[Iterable[TaskUsageStatus]] = None,
    ):
        """
        Generate Group Report (Task Usage).

        `words_count_from` and `words_count_to` are used only with `time` type, `statuses` only
        with `cost` type. `type_task` is sent as `typeTasks`.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-task-usage",
                "schema": {
                    "format": format,
                    "type": type,
                    "projectIds": project_ids,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "groupBy": group_by,
                    "typeTasks": type_task,
                    "languageId": language_id,
                    "creatorId": creator_id,
                    "assigneeId": assignee_id,
                    "wordsCountFrom": words_count_from,
                    "wordsCountTo": words_count_to,
                    "statuses": statuses,
                },
            },
        )

    def generate_group_qa_check_issues_report(
        self,
        group_id: int,
        project_ids: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """
        Generate Group Report (Qa Check Issues).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-qa-check-issues",
                "schema": {
                    "projectIds": project_ids,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_group_translation_activity_report(
        self,
        group_id: int,
        unit: Optional[Unit] = None,
        project_ids: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        user_ids: Optional[Iterable[int]] = None,
    ):
        """
        Generate Group Report (Translation Activity).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-translation-activity",
                "schema": {
                    "unit": unit,
                    "projectIds": project_ids,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids,
                },
            },
        )

    def generate_group_source_content_updates_report(
        self,
        group_id: int,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        project_ids: Optional[Iterable[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """
        Generate Group Report (Source Content Updates).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-source-content-updates",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "projectIds": project_ids,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_group_time_spent_report(
        self,
        group_id: int,
        format: Optional[Format] = None,
        group_by: Optional[GroupBy] = None,
        base_rates: Optional[HourlyBaseRates] = None,
        individual_rates: Optional[Iterable[HourlyIndividualRate]] = None,
        language_id: Optional[str] = None,
        user_ids: Optional[Iterable[int]] = None,
        type_tasks: Optional[TaskType] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        project_ids: Optional[Iterable[int]] = None,
        task_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Group Report (Time Spent).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-time-spent",
                "schema": {
                    "format": format,
                    "groupBy": group_by,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "languageId": language_id,
                    "userIds": user_ids,
                    "typeTasks": type_tasks,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "projectIds": project_ids,
                    "taskIds": task_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_group_pre_translate_accuracy_general_report(
        self,
        group_id: int,
        unit: Optional[Unit] = None,
        language_id: Optional[str] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        match_score_categories: Optional[Iterable[str]] = None,
        project_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Group Report (Pre-Translate Accuracy General).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-pre-translate-accuracy",
                "schema": {
                    "unit": unit,
                    "languageId": language_id,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "matchScoreCategories": match_score_categories,
                    "projectIds": project_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_group_pre_translate_accuracy_by_task_report(
        self,
        group_id: int,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        match_score_categories: Optional[Iterable[str]] = None,
        task_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Group Report (Pre-Translate Accuracy By Task).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-pre-translate-accuracy",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "matchScoreCategories": match_score_categories,
                    "taskIds": task_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_group_translator_accuracy_report(
        self,
        group_id: int,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        language_id: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        match_score_categories: Optional[Iterable[str]] = None,
        user_ids: Optional[Iterable[int]] = None,
        project_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Group Report (Translator Accuracy).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-translator-accuracy",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "languageId": language_id,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "matchScoreCategories": match_score_categories,
                    "userIds": user_ids,
                    "projectIds": project_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_group_saving_activity_report(
        self,
        group_id: int,
        unit: Optional[Unit] = None,
        project_ids: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        language_id: Optional[str] = None,
        mode: Optional[SavingActivityMode] = None,
    ):
        """
        Generate Group Report (Saving Activity).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.groups.reports.post
        """

        return self.generate_group_report(
            group_id=group_id,
            request_data={
                "name": "group-saving-activity",
                "schema": {
                    "unit": unit,
                    "projectIds": project_ids,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "languageId": language_id,
                    "mode": mode,
                },
            },
        )

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
        user_ids: Optional[Iterable[int]] = None,
        use_category_based_proofread_rates: Optional[bool] = None,
        use_tm_edit_distance: Optional[bool] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Organization Report (Translation Costs Post-Editing General).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-translation-costs-pe",
                "schema": {
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "projectIds": project_ids,
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "groupBy": group_by,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids,
                    "useCategoryBasedProofreadRates": use_category_based_proofread_rates,
                    "useTmEditDistance": use_tm_edit_distance,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_organization_translation_costs_post_editing_by_task_report(
        self,
        base_rates: BaseRates,
        individual_rates: Iterable[TranslationCostsPeIndividualRate],
        net_rate_schemes: TranslationCostsPeNetRateSchemes,
        unit: Optional[Unit] = None,
        currency: Optional[Currency] = None,
        format: Optional[Format] = None,
        task_ids: Optional[Iterable[int]] = None,
        use_category_based_proofread_rates: Optional[bool] = None,
        use_tm_edit_distance: Optional[bool] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Organization Report (Translation Costs Post-Editing By Task).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-translation-costs-pe",
                "schema": {
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "netRateSchemes": net_rate_schemes,
                    "unit": unit,
                    "currency": currency,
                    "format": format,
                    "taskIds": task_ids,
                    "useCategoryBasedProofreadRates": use_category_based_proofread_rates,
                    "useTmEditDistance": use_tm_edit_distance,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_organization_top_members_report(
        self,
        project_ids: Optional[Iterable[int]] = None,
        unit: Optional[Unit] = None,
        language_id: Optional[str] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        user_ids: Optional[Iterable[int]] = None,
    ):
        """
        Generate Organization Report (Top Members).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-top-members",
                "schema": {
                    "projectIds": project_ids,
                    "unit": unit,
                    "languageId": language_id,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids,
                },
            },
        )

    def generate_organization_task_usage_report(
        self,
        format: Optional[Format] = None,
        type: Optional[TaskUsageReportType] = None,
        project_ids: Optional[Iterable[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        group_by: Optional[GroupBy] = None,
        type_tasks: Optional[TaskType] = None,
        language_id: Optional[str] = None,
        creator_id: Optional[int] = None,
        assignee_id: Optional[int] = None,
        words_count_from: Optional[int] = None,
        words_count_to: Optional[int] = None,
        statuses: Optional[Iterable[TaskUsageStatus]] = None,
    ):
        """
        Generate Organization Report (Task Usage).

        `words_count_from` and `words_count_to` are used only with `time` type, `statuses` only
        with `cost` type.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-task-usage",
                "schema": {
                    "format": format,
                    "type": type,
                    "projectIds": project_ids,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "groupBy": group_by,
                    "typeTasks": type_tasks,
                    "languageId": language_id,
                    "creatorId": creator_id,
                    "assigneeId": assignee_id,
                    "wordsCountFrom": words_count_from,
                    "wordsCountTo": words_count_to,
                    "statuses": statuses,
                },
            },
        )

    def generate_organization_qa_check_issues_report(
        self,
        project_ids: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """
        Generate Organization Report (Qa Check Issues).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-qa-check-issues",
                "schema": {
                    "projectIds": project_ids,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_organization_translation_activity_report(
        self,
        unit: Optional[Unit] = None,
        project_ids: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        user_ids: Optional[Iterable[int]] = None,
    ):
        """
        Generate Organization Report (Translation Activity).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-translation-activity",
                "schema": {
                    "unit": unit,
                    "projectIds": project_ids,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "userIds": user_ids,
                },
            },
        )

    def generate_organization_source_content_updates_report(
        self,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        project_ids: Optional[Iterable[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        """
        Generate Organization Report (Source Content Updates).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-source-content-updates",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "projectIds": project_ids,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                },
            },
        )

    def generate_organization_time_spent_report(
        self,
        format: Optional[Format] = None,
        group_by: Optional[GroupBy] = None,
        base_rates: Optional[HourlyBaseRates] = None,
        individual_rates: Optional[Iterable[HourlyIndividualRate]] = None,
        language_id: Optional[str] = None,
        user_ids: Optional[Iterable[int]] = None,
        type_tasks: Optional[TaskType] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        project_ids: Optional[Iterable[int]] = None,
        task_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Organization Report (Time Spent).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-time-spent",
                "schema": {
                    "format": format,
                    "groupBy": group_by,
                    "baseRates": base_rates,
                    "individualRates": individual_rates,
                    "languageId": language_id,
                    "userIds": user_ids,
                    "typeTasks": type_tasks,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "projectIds": project_ids,
                    "taskIds": task_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_organization_pre_translate_accuracy_general_report(
        self,
        unit: Optional[Unit] = None,
        language_id: Optional[str] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        match_score_categories: Optional[Iterable[str]] = None,
        project_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Organization Report (Pre-Translate Accuracy General).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-pre-translate-accuracy",
                "schema": {
                    "unit": unit,
                    "languageId": language_id,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "matchScoreCategories": match_score_categories,
                    "projectIds": project_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_organization_pre_translate_accuracy_by_task_report(
        self,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        match_score_categories: Optional[Iterable[str]] = None,
        task_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Organization Report (Pre-Translate Accuracy By Task).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-pre-translate-accuracy",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "matchScoreCategories": match_score_categories,
                    "taskIds": task_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_organization_translator_accuracy_report(
        self,
        unit: Optional[Unit] = None,
        format: Optional[Format] = None,
        language_id: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        match_score_categories: Optional[Iterable[str]] = None,
        user_ids: Optional[Iterable[int]] = None,
        project_ids: Optional[Iterable[int]] = None,
        skip_archiving: Optional[bool] = None,
    ):
        """
        Generate Organization Report (Translator Accuracy).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-translator-accuracy",
                "schema": {
                    "unit": unit,
                    "format": format,
                    "languageId": language_id,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "matchScoreCategories": match_score_categories,
                    "userIds": user_ids,
                    "projectIds": project_ids,
                    "skipArchiving": skip_archiving,
                },
            },
        )

    def generate_organization_saving_activity_report(
        self,
        unit: Optional[Unit] = None,
        project_ids: Optional[Iterable[int]] = None,
        format: Optional[Format] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        language_id: Optional[str] = None,
        mode: Optional[SavingActivityMode] = None,
    ):
        """
        Generate Organization Report (Saving Activity).

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.reports.post
        """

        return self.generate_organization_report(
            request_data={
                "name": "group-saving-activity",
                "schema": {
                    "unit": unit,
                    "projectIds": project_ids,
                    "format": format,
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "languageId": language_id,
                    "mode": mode,
                },
            },
        )
