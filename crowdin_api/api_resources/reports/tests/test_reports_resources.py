from datetime import datetime
from unittest import mock
import warnings

import pytest

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.reports.enums import (
    ExportFormat,
    ScopeType,
    ContributionMode,
    Currency,
    Format,
    GroupBy,
    SimpleRateMode,
    Unit,
    ReportSettingsTemplatesPatchPath,
    MatchType,
    ReportLabelIncludeType,
    TaskType,
    TaskUsageReportType,
    TaskUsageStatus,
)
from crowdin_api.api_resources.reports.requests.cost_estimation_post_editing import (
    IndividualRate,
    NetRateSchemes
)
from crowdin_api.api_resources.reports.requests.group_translation_costs_post_editing import (
    IndividualRate as GroupIndividualRate,
    NetRateSchemes as GroupNetRateSchemes
)
from crowdin_api.api_resources.reports.resource import (
    ReportsResource,
    EnterpriseReportsResource,
    BaseReportSettingsTemplatesResource,
)
from crowdin_api.api_resources.reports.types import BaseRates, Match
from crowdin_api.requester import APIRequester

from crowdin_api.api_resources.reports.resource import UserReportSettingsTemplatesResource


class TestReportsResource:
    resource_class = ReportsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"userId": 1}, "users/1/reports/archives"),
            ({"userId": 1, "archiveId": 1}, "users/1/reports/archives/1"),
        ),
    )
    def test_get_report_archive_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_report_archive_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"userId": 1, "archiveId": 1}, "users/1/reports/archives/1/exports"),
            (
                {"userId": 1, "archiveId": 1, "exportId": "exportId"},
                "users/1/reports/archives/1/exports/exportId",
            ),
        ),
    )
    def test_get_report_archive_export_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_report_archive_export_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "scopeType": None,
                    "scopeId": None,
                    "limit": 25,
                    "offset": 0,
                    "taskId": None,
                    "name": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "scopeType": "project",
                    "scopeId": 1,
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "scopeType": "project",
                    "scopeId": 1,
                    "limit": 10,
                    "offset": 2,
                    "taskId": None,
                    "name": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_report_archives(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        userId = 1
        assert resource.list_report_archives(userId=userId, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_archive_path(userId=userId),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_report_archive(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        userId = 1
        archiveId = 2
        assert (
            resource.get_report_archive(userId=userId, archiveId=archiveId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_archive_path(userId=userId, archiveId=archiveId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_report_archive(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        userId = 1
        archiveId = 2
        assert (
            resource.delete_report_archive(userId=userId, archiveId=archiveId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_report_archive_path(userId=userId, archiveId=archiveId),
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {},
                {"format": ExportFormat.XLSX},
            ),
            (
                {"format": ExportFormat.CSV},
                {"format": ExportFormat.CSV},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_report_archive(
        self, m_request, incoming_data, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        userId = 1
        archiveId = 2
        assert (
            resource.export_report_archive(
                userId=userId, archiveId=archiveId, **incoming_data
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_report_archive_export_path(
                userId=userId, archiveId=archiveId
            ),
            request_data=request_data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_report_archive_export_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        userId = 1
        archiveId = 2
        exportId = "exportId"
        assert (
            resource.check_report_archive_export_status(
                userId=userId, archiveId=archiveId, exportId=exportId
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_archive_export_path(
                userId=userId, archiveId=archiveId, exportId=exportId
            ),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_report_archive(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        userId = 1
        archiveId = 2
        exportId = "exportId"
        assert (
            resource.download_report_archive(
                userId=userId, archiveId=archiveId, exportId=exportId
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=str(
                resource.get_report_archive_export_path(
                    userId=userId, archiveId=archiveId, exportId=exportId
                )
                + "/download"
            ),
        )

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1}, "projects/1/reports"),
            ({"projectId": 1, "reportId": "hash"}, "projects/1/reports/hash"),
        ),
    )
    def test_get_reports_path(self, incoming_data, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_reports_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "name_method",
        [
            # BaseReportSettingsTemplatesResource methods
            "get_report_settings_templates_path",
            "list_report_settings_template",
            "add_report_settings_template",
            "get_report_settings_template",
            "delete_report_settings_template",
        ]
    )
    def test_present_methods(self, name_method):
        assert hasattr(self.resource_class, name_method)

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        request_data = {"some_key": "some_value"}
        resource = self.get_resource(base_absolut_url)
        assert resource.generate_report(projectId=1, request_data=request_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_reports_path(projectId=1),
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "mode": "simple",
                    "languageId": None,
                    "fileIds": None,
                    "format": Format.XLSX,
                    "regularRates": None,
                    "individualRates": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "mode": "simple",
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_simple_cost_estimate_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert resource.generate_simple_cost_estimate_report(projectId=1, **in_params) == "response"
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "costs-estimation", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "mode": "fuzzy",
                    "languageId": None,
                    "fileIds": None,
                    "format": Format.XLSX,
                    "calculateInternalFuzzyMatches": None,
                    "regularRates": None,
                    "individualRates": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "calculateInternalFuzzyMatches": False,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "mode": "fuzzy",
                    "currency": Currency.UAH,
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "calculateInternalFuzzyMatches": False,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_fuzzy_cost_estimate_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert resource.generate_fuzzy_cost_estimate_report(projectId=1, **in_params) == "response"
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "costs-estimation", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "mode": "simple",
                    "groupBy": None,
                    "format": Format.XLSX,
                    "regularRates": None,
                    "individualRates": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "mode": "simple",
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_simple_translation_cost_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert (
            resource.generate_simple_translation_cost_report(projectId=1, **in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "translation-costs", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "mode": "fuzzy",
                    "groupBy": None,
                    "format": Format.XLSX,
                    "regularRates": None,
                    "individualRates": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "mode": "fuzzy",
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                    "individualRates": [
                        {
                            "languageIds": ["ua"],
                            "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                        }
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_fuzzy_translation_cost_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert (
            resource.generate_fuzzy_translation_cost_report(projectId=1, **in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "translation-costs", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "languageId": None,
                    "format": Format.XLSX,
                    "dateFrom": None,
                    "dateTo": None,
                    "userIds": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "format": Format.JSON,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "format": Format.JSON,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "userIds": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_top_members_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_top_members_report(projectId=1, **in_params) == "response"
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "top-members", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {"mode": ContributionMode.VOTES},
                {
                    "mode": ContributionMode.VOTES,
                    "unit": None,
                    "languageId": None,
                    "userId": None,
                    "dateFrom": None,
                    "dateTo": None,
                    "columns": None,
                    "tmIds": None,
                    "mtIds": None,
                    "aiPromptIds": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                },
            ),
            (
                {
                    "mode": ContributionMode.VOTES,
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "userId": 1,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "mode": ContributionMode.VOTES,
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "userId": 1,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "columns": None,
                    "tmIds": None,
                    "mtIds": None,
                    "aiPromptIds": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_contribution_raw_data_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_contribution_raw_data_report(projectId=1, **in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={"name": "contribution-raw-data", "schema": schema},
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                },
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "date_from": datetime(2023, 1, 1),
                    "date_to": datetime(2023, 12, 31),
                },
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "dateFrom": datetime(2023, 1, 1),
                    "dateTo": datetime(2023, 12, 31),
                },
            ),
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_source_content_updates_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        result = resource.generate_source_content_updates_report(project_id=1, **in_params)
        assert result == "response"

        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={
                "name": "source-content-updates",
                "schema": expected_schema,
            },
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {"format": Format.XLSX},
                {
                    "format": Format.XLSX,
                    "dateFrom": None,
                    "dateTo": None
                },
            ),
            (
                {
                    "format": Format.XLSX,
                    "date_from": datetime(2023, 1, 1),
                    "date_to": datetime(2023, 12, 31),
                },
                {
                    "format": Format.XLSX,
                    "dateFrom": datetime(2023, 1, 1),
                    "dateTo": datetime(2023, 12, 31),
                },
            ),
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_project_members_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        result = resource.generate_project_members_report(project_id=1, **in_params)
        assert result == "response"

        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={"name": "project-members", "schema": expected_schema},
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {},
                {
                    "dateFrom": None,
                    "dateTo": None,
                    "format": Format.XLSX,
                    "issueType": None
                },
            ),
            (
                {
                    "date_from": datetime(2022, 5, 1),
                    "date_to": datetime(2022, 6, 1),
                    "format": Format.XLSX,
                    "issue_type": "uncategorized",
                },
                {
                    "dateFrom": datetime(2022, 5, 1),
                    "dateTo": datetime(2022, 6, 1),
                    "format": Format.XLSX,
                    "issueType": "uncategorized",
                },
            ),
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_editor_issues_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        result = resource.generate_editor_issues_report(project_id=1, **in_params)
        assert result == "response"
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={"name": "editor-issues", "schema": expected_schema},
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {},
                {
                    "format": Format.XLSX,
                    "dateFrom": None,
                    "dateTo": None,
                    "languageId": None,
                },
            ),
            (
                {
                    "format": Format.XLSX,
                    "date_from": datetime(2023, 4, 1),
                    "date_to": datetime(2023, 4, 30),
                },
                {
                    "format": Format.XLSX,
                    "dateFrom": datetime(2023, 4, 1),
                    "dateTo": datetime(2023, 4, 30),
                    "languageId": None,
                },
            ),
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_qa_check_issues_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        result = resource.generate_qa_check_issues_report(project_id=1, **in_params)
        assert result == "response"

        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={"name": "qa-check-issues", "schema": expected_schema},
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "language_id": "uk"
                },
                {
                    "unit": Unit.WORDS,
                    "languageId": "uk",
                    "format": Format.XLSX,
                    "dateFrom": None,
                    "dateTo": None,
                    "mode": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                    "userIds": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "language_id": "de",
                    "format": Format.XLSX,
                    "date_from": datetime(2023, 2, 1),
                    "date_to": datetime(2023, 2, 28),
                },
                {
                    "unit": Unit.WORDS,
                    "languageId": "de",
                    "format": Format.XLSX,
                    "dateFrom": datetime(2023, 2, 1),
                    "dateTo": datetime(2023, 2, 28),
                    "mode": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                    "userIds": None,
                },
            ),
        ]
    )
    @mock.patch(
        "crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report"
    )
    def test_generate_saving_activity_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        result = resource.generate_saving_activity_report(project_id=1, **in_params)
        assert result == "response"

        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={"name": "saving-activity", "schema": expected_schema},
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "postEditingCategories": ["0-20", "20-50"],
                    "languageId": "uk",
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "postEditingCategories": ["0-20", "20-50"],
                    "languageId": "uk",
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "matchScoreCategories": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                    "labelIds": None,
                    "labelIncludeType": None,
                    "skipArchiving": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "languageId": "uk",
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "postEditingCategories": None,
                    "languageId": "uk",
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "matchScoreCategories": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                    "labelIds": None,
                    "labelIncludeType": None,
                    "skipArchiving": None,
                },
            )
        ],
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_pre_translate_accuracy_general_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_pre_translate_accuracy_general_report(
                projectId=1,
                **in_params
            ) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={
                "name": "pre-translate-accuracy",
                "schema": schema
            }
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "postEditingCategories": ["0-20", "20-50"],
                    "taskId": 1
                },
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "postEditingCategories": ["0-20", "20-50"],
                    "taskId": 1,
                    "matchScoreCategories": None,
                    "skipArchiving": None,
                }
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "taskId": 1
                },
                {
                    "unit": Unit.WORDS,
                    "format": Format.XLSX,
                    "postEditingCategories": None,
                    "taskId": 1,
                    "matchScoreCategories": None,
                    "skipArchiving": None,
                }
            )
        ]
    )
    @mock.patch(
        "crowdin_api.api_resources.reports.resource.ReportsResource.generate_report"
    )
    def test_generate_pre_translate_accuracy_by_task_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_pre_translate_accuracy_by_task_report(
                projectId=1,
                **in_params
            ) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={
                "name": "pre-translate-accuracy",
                "schema": schema
            }
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "base_rates": BaseRates(fullTranslation=0, proofread=0),
                    "individual_rates": [
                        IndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "net_rate_schemes": NetRateSchemes(tmMatch=[
                        Match(matchType=MatchType.OPTION_100, price=70)
                    ]),
                    "calculate_internal_matches": True,
                    "include_pre_translated_strings": True,
                    "language_id": "uk",
                    "file_ids": [1, 2],
                    "directory_ids": [1, 2],
                    "branch_ids": [1, 2],
                    "date_from": datetime(year=1988, month=1, day=4),
                    "date_to": datetime(year=2015, month=10, day=13),
                    "label_ids": [1],
                    "label_include_type": ReportLabelIncludeType.STRINGS_WITH_LABEL
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "baseRates": {
                        "fullTranslation": 0,
                        "proofread": 0
                    },
                    "individualRates": [
                        {
                            "languageIds": ["uk"],
                            "userIds": [1],
                            "fullTranslation": 0.1,
                            "proofread": 0.1
                        }
                    ],
                    "netRateSchemes": {
                        "tmMatch": [
                            {
                                "matchType": MatchType.OPTION_100,
                                "price": 70
                            }
                        ]
                    },
                    "calculateInternalMatches": True,
                    "includePreTranslatedStrings": True,
                    "languageId": "uk",
                    "fileIds": [1, 2],
                    "directoryIds": [1, 2],
                    "branchIds": [1, 2],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "labelIds": [1],
                    "labelIncludeType": ReportLabelIncludeType.STRINGS_WITH_LABEL,
                    "skipArchiving": None,
                    "workflowStepId": None,
                }
            )
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_costs_estimation_post_editing_general_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_costs_estimation_post_editing_general_report(
                project_id=1,
                **in_params
            ) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={
                "name": "costs-estimation-pe",
                "schema": schema
            }
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "base_rates": BaseRates(fullTranslation=0, proofread=0),
                    "individual_rates": [
                        IndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "net_rate_schemes": NetRateSchemes(tmMatch=[
                        Match(matchType=MatchType.OPTION_100, price=70)
                    ]),
                    "calculate_internal_matches": True,
                    "include_pre_translated_strings": True,
                    "task_id": 1
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "baseRates": {
                        "fullTranslation": 0,
                        "proofread": 0
                    },
                    "individualRates": [
                        {
                            "languageIds": ["uk"],
                            "userIds": [1],
                            "fullTranslation": 0.1,
                            "proofread": 0.1
                        }
                    ],
                    "netRateSchemes": {
                        "tmMatch": [
                            {
                                "matchType": MatchType.OPTION_100,
                                "price": 70
                            }
                        ]
                    },
                    "calculateInternalMatches": True,
                    "includePreTranslatedStrings": True,
                    "taskId": 1,
                    "taskIds": None,
                    "skipArchiving": None,
                }
            )
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_costs_estimation_post_editing_by_task_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_costs_estimation_post_editing_by_task_report(
                project_id=1,
                **in_params
            ) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={
                "name": "costs-estimation-pe",
                "schema": schema
            }
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "base_rates": BaseRates(fullTranslation=0, proofread=0),
                    "individual_rates": [
                        IndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "net_rate_schemes": NetRateSchemes(tmMatch=[
                        Match(matchType=MatchType.OPTION_99_82, price=70)
                    ]),
                    "group_by": GroupBy.LANGUAGE,
                    "date_from": datetime(year=1988, month=1, day=4),
                    "date_to": datetime(year=2015, month=10, day=13),
                    "language_id": "uk",
                    "user_ids": [1],
                    "file_ids": [1],
                    "directory_ids": [1],
                    "branch_ids": [1]
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "baseRates": BaseRates(fullTranslation=0, proofread=0),
                    "individualRates": [
                        IndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "netRateSchemes": NetRateSchemes(tmMatch=[
                        Match(matchType=MatchType.OPTION_99_82, price=70)
                    ]),
                    "groupBy": GroupBy.LANGUAGE,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "languageId": "uk",
                    "userIds": [1],
                    "fileIds": [1],
                    "directoryIds": [1],
                    "branchIds": [1],
                    "useCategoryBasedProofreadRates": None,
                    "useTmEditDistance": None,
                    "labelIds": None,
                    "labelIncludeType": None,
                    "skipArchiving": None,
                    "workflowStepId": None,
                }
            )
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_translation_costs_post_editing_general_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_translation_costs_post_editing_general_report(
                project_id=1,
                **in_params
            ) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={
                "name": "translation-costs-pe",
                "schema": schema
            }
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "base_rates": BaseRates(fullTranslation=0, proofread=0),
                    "individual_rates": [
                        IndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "net_rate_schemes": NetRateSchemes(tmMatch=[
                        Match(matchType=MatchType.OPTION_99_82, price=70)
                    ]),
                    "task_id": 1
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "baseRates": BaseRates(fullTranslation=0, proofread=0),
                    "individualRates": [
                        IndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "netRateSchemes": NetRateSchemes(tmMatch=[
                        Match(matchType=MatchType.OPTION_99_82, price=70)
                    ]),
                    "taskId": 1,
                    "taskIds": None,
                    "useCategoryBasedProofreadRates": None,
                    "useTmEditDistance": None,
                    "skipArchiving": None,
                }
            )
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.ReportsResource.generate_report")
    def test_generate_translation_costs_post_editing_by_task_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_translation_costs_post_editing_by_task_report(
                project_id=1,
                **in_params
            ) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={
                "name": "translation-costs-pe",
                "schema": schema
            }
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_report_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_report_generation_status(projectId=1, reportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_reports_path(projectId=1, reportId="hash")
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_report(projectId=1, reportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_reports_path(projectId=1, reportId="hash") + "/download",
        )


class TestEnterpriseReportsResource:
    resource_class = EnterpriseReportsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1}, "projects/1/reports"),
            ({"projectId": 1, "reportId": "hash"}, "projects/1/reports/hash"),
        ),
    )
    def test_get_reports_path(self, incoming_data, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_reports_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "name_method",
        [
            # BaseReportSettingsTemplatesResource methods
            "get_report_settings_templates_path",
            "list_report_settings_template",
            "add_report_settings_template",
            "get_report_settings_template",
            "delete_report_settings_template",
        ]
    )
    def test_present_methods(self, name_method):
        assert hasattr(self.resource_class, name_method)

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({}, "reports/archives"),
            ({"archiveId": 1}, "reports/archives/1"),
        ),
    )
    def test_get_report_archive_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_report_archive_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"archiveId": 1}, "reports/archives/1/exports"),
            (
                {"archiveId": 1, "exportId": "exportId"},
                "reports/archives/1/exports/exportId",
            ),
        ),
    )
    def test_get_report_archive_export_path(
        self, incoming_data, path, base_absolut_url
    ):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_report_archive_export_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "scopeType": None,
                    "scopeId": None,
                    "limit": 25,
                    "offset": 0,
                    "userId": None,
                    "taskId": None,
                    "name": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "scopeType": ScopeType.GRPOUP,
                    "scopeId": 1,
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "scopeType": ScopeType.GRPOUP,
                    "scopeId": 1,
                    "limit": 10,
                    "offset": 2,
                    "userId": None,
                    "taskId": None,
                    "name": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_report_archives(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_report_archives(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_archive_path(),
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_report_archive(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        archiveId = 1
        assert resource.get_report_archive(archiveId=archiveId) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_archive_path(archiveId=archiveId),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_report_archive(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        archiveId = 1
        assert resource.delete_report_archive(archiveId=archiveId) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_report_archive_path(archiveId=archiveId),
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {},
                {"format": ExportFormat.XLSX},
            ),
            (
                {"format": ExportFormat.CSV},
                {"format": ExportFormat.CSV},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_export_report_archive(
        self, m_request, incoming_data, request_data, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        archiveId = 1
        assert (
            resource.export_report_archive(archiveId=archiveId, **incoming_data)
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_report_archive_export_path(archiveId=archiveId),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_report_archive_export_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        archiveId = 1
        exportId = "exportId"
        assert (
            resource.check_report_archive_export_status(
                archiveId=archiveId, exportId=exportId
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_archive_export_path(
                archiveId=archiveId, exportId=exportId
            ),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_report_archive(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        archiveId = 1
        exportId = "exportId"
        assert (
            resource.download_report_archive(archiveId=archiveId, exportId=exportId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=str(
                resource.get_report_archive_export_path(
                    archiveId=archiveId, exportId=exportId
                )
                + "/download"
            ),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        request_data = {"some_key": "some_value"}
        resource = self.get_resource(base_absolut_url)
        assert resource.generate_report(projectId=1, request_data=request_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_reports_path(projectId=1),
            request_data=request_data,
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "languageId": None,
                    "fileIds": None,
                    "format": Format.XLSX,
                    "stepTypes": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {"stepTypes": "NOT_VALID_FORMAT"},
                {
                    "unit": None,
                    "currency": None,
                    "languageId": None,
                    "fileIds": None,
                    "format": Format.XLSX,
                    "stepTypes": "NOT_VALID_FORMAT",
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "type": "Translate",
                            "mode": "simple",
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_simple_cost_estimate_report(
        self, mock_generate_report, in_params, schema, base_absolut_url
    ):
        mock_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert resource.generate_simple_cost_estimate_report(projectId=1, **in_params) == "response"
        mock_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "costs-estimation", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "languageId": None,
                    "fileIds": None,
                    "format": Format.XLSX,
                    "stepTypes": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {"stepTypes": "NOT_VALID_FORMAT"},
                {
                    "unit": None,
                    "currency": None,
                    "languageId": None,
                    "fileIds": None,
                    "format": Format.XLSX,
                    "stepTypes": "NOT_VALID_FORMAT",
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "languageId": "ua",
                    "fileIds": [1, 2, 3],
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "type": "Translate",
                            "mode": "fuzzy",
                            "calculateInternalFuzzyMatches": False,
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_fuzzy_cost_estimate_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert resource.generate_fuzzy_cost_estimate_report(projectId=1, **in_params) == "response"
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "costs-estimation", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "groupBy": None,
                    "format": Format.XLSX,
                    "stepTypes": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {"stepTypes": "NOT_VALID_FORMAT"},
                {
                    "unit": None,
                    "currency": None,
                    "groupBy": None,
                    "format": Format.XLSX,
                    "stepTypes": "NOT_VALID_FORMAT",
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "type": "Translate",
                            "mode": "simple",
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_simple_translation_cost_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert (
            resource.generate_simple_translation_cost_report(projectId=1, **in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "translation-costs", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "currency": None,
                    "groupBy": None,
                    "format": Format.XLSX,
                    "stepTypes": None,
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {"stepTypes": "NOT_VALID_FORMAT"},
                {
                    "unit": None,
                    "currency": None,
                    "groupBy": None,
                    "format": Format.XLSX,
                    "stepTypes": "NOT_VALID_FORMAT",
                    "dateFrom": None,
                    "dateTo": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "groupBy": GroupBy.USER,
                    "format": Format.JSON,
                    "stepTypes": [
                        {
                            "type": "Translate",
                            "mode": "fuzzy",
                            "regularRates": [{"mode": SimpleRateMode.TM_MATCH, "value": 1}],
                            "individualRates": [
                                {
                                    "languageIds": ["ua"],
                                    "rates": {"mode": SimpleRateMode.TM_MATCH, "value": 1},
                                }
                            ]}
                    ],
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_fuzzy_translation_cost_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        assert (
            resource.generate_fuzzy_translation_cost_report(projectId=1, **in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "translation-costs", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {},
                {
                    "unit": None,
                    "languageId": None,
                    "format": Format.XLSX,
                    "dateFrom": None,
                    "dateTo": None,
                    "userIds": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "format": Format.JSON,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "format": Format.JSON,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "userIds": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_top_members_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_top_members_report(projectId=1, **in_params) == "response"
        m_generate_report.assert_called_once_with(
            projectId=1, request_data={"name": "top-members", "schema": schema}
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        (
            (
                {"mode": ContributionMode.VOTES},
                {
                    "mode": ContributionMode.VOTES,
                    "unit": None,
                    "languageId": None,
                    "userId": None,
                    "dateFrom": None,
                    "dateTo": None,
                    "columns": None,
                    "tmIds": None,
                    "mtIds": None,
                    "aiPromptIds": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                },
            ),
            (
                {
                    "mode": ContributionMode.VOTES,
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "userId": 1,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                },
                {
                    "mode": ContributionMode.VOTES,
                    "unit": Unit.WORDS,
                    "languageId": "ua",
                    "userId": 1,
                    "dateFrom": datetime(year=1988, month=1, day=4),
                    "dateTo": datetime(year=2015, month=10, day=13),
                    "columns": None,
                    "tmIds": None,
                    "mtIds": None,
                    "aiPromptIds": None,
                    "fileIds": None,
                    "directoryIds": None,
                    "branchIds": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
    def test_generate_contribution_raw_data_report(
        self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_contribution_raw_data_report(projectId=1, **in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            projectId=1,
            request_data={"name": "contribution-raw-data", "schema": schema},
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "project_ids": [1, 2, 3],
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "base_rates": BaseRates(fullTranslation=0, proofread=0),
                    "individual_rates": [
                        GroupIndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "net_rate_schemes": GroupNetRateSchemes(
                        tmMatch=[
                            Match(matchType=MatchType.OPTION_100, price=70)
                        ],
                        mtMatch=[
                            Match(matchType=MatchType.OPTION_99_82, price=50)
                        ],
                        suggestionMatch=[
                            Match(matchType=MatchType.OPTION_81_60, price=30)
                        ]
                    ),
                    "group_by": GroupBy.LANGUAGE,
                    "date_from": None,
                    "date_to": None,
                    "user_ids": [10, 11]
                },
                {
                    "projectIds": [1, 2, 3],
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "baseRates": {
                        "fullTranslation": 0,
                        "proofread": 0
                    },
                    "individualRates": [
                        {
                            "languageIds": ["uk"],
                            "userIds": [1],
                            "fullTranslation": 0.1,
                            "proofread": 0.1
                        }
                    ],
                    "netRateSchemes": {
                        "tmMatch": [
                            {
                                "matchType": MatchType.OPTION_100,
                                "price": 70
                            }
                        ],
                        "mtMatch": [
                            {
                                "matchType": MatchType.OPTION_99_82,
                                "price": 50
                            }
                        ],
                        "suggestionMatch": [
                            {
                                "matchType": MatchType.OPTION_81_60,
                                "price": 30
                            }
                        ]
                    },
                    "groupBy": GroupBy.LANGUAGE,
                    "dateFrom": None,
                    "dateTo": None,
                    "userIds": [10, 11],
                    "useCategoryBasedProofreadRates": None,
                    "useTmEditDistance": None,
                    "skipArchiving": None,
                }
            )
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.EnterpriseReportsResource.generate_group_report")
    def test_generate_group_translation_costs_post_editing_general_report(
            self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_group_translation_costs_post_editing_general_report(group_id=1, **in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            group_id=1,
            request_data={"name": "group-translation-costs-pe", "schema": schema},
        )

    @pytest.mark.parametrize(
        "in_params, schema",
        [
            (
                {
                    "project_ids": [1, 2, 3],
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "base_rates": BaseRates(fullTranslation=0, proofread=0),
                    "individual_rates": [
                        GroupIndividualRate(languageIds=["uk"], userIds=[1], fullTranslation=0.1, proofread=0.1)
                    ],
                    "net_rate_schemes": GroupNetRateSchemes(
                        tmMatch=[
                            Match(matchType=MatchType.OPTION_100, price=70)
                        ],
                        mtMatch=[
                            Match(matchType=MatchType.OPTION_99_82, price=50)
                        ],
                        suggestionMatch=[
                            Match(matchType=MatchType.OPTION_81_60, price=30)
                        ]
                    ),
                    "group_by": GroupBy.LANGUAGE,
                    "date_from": None,
                    "date_to": None,
                    "user_ids": [10, 11]
                },
                {
                    "projectIds": [1, 2, 3],
                    "unit": Unit.WORDS,
                    "currency": Currency.UAH,
                    "format": Format.XLSX,
                    "baseRates": {
                        "fullTranslation": 0,
                        "proofread": 0
                    },
                    "individualRates": [
                        {
                            "languageIds": ["uk"],
                            "userIds": [1],
                            "fullTranslation": 0.1,
                            "proofread": 0.1
                        }
                    ],
                    "netRateSchemes": {
                        "tmMatch": [
                            {
                                "matchType": MatchType.OPTION_100,
                                "price": 70
                            }
                        ],
                        "mtMatch": [
                            {
                                "matchType": MatchType.OPTION_99_82,
                                "price": 50
                            }
                        ],
                        "suggestionMatch": [
                            {
                                "matchType": MatchType.OPTION_81_60,
                                "price": 30
                            }
                        ]
                    },
                    "groupBy": GroupBy.LANGUAGE,
                    "dateFrom": None,
                    "dateTo": None,
                    "userIds": [10, 11],
                    "useCategoryBasedProofreadRates": None,
                    "useTmEditDistance": None,
                    "skipArchiving": None,
                }
            )
        ]
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_organization_translation_costs_post_editing_general_report(
            self, m_generate_report, in_params, schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.generate_organization_translation_costs_post_editing_general_report(**in_params) == "response"
        )
        m_generate_report.assert_called_once_with(
            method="post",
            path="reports",
            request_data={"name": "group-translation-costs-pe", "schema": schema},
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {
                    "format": Format.XLSX,
                    "type": "all"
                },
                {
                    "projectIds": None,
                    "format": Format.XLSX,
                    "type": "all",
                    "dateFrom": None,
                    "dateTo": None,
                    "groupBy": None,
                    "typeTasks": None,
                    "languageId": None,
                    "creatorId": None,
                    "assigneeId": None,
                    "wordsCountFrom": None,
                    "wordsCountTo": None,
                    "statuses": None,
                },
            ),
            (
                {
                    "project_ids": [1],
                    "format": Format.XLSX,
                    "type": "translate",
                    "date_from": datetime(2023, 1, 1),
                    "date_to": datetime(2023, 12, 31),
                    "group_by": GroupBy.USER,
                    "type_task": 2,
                    "language_id": "uk",
                    "creator_id": 10,
                    "assignee_id": 20,
                },
                {
                    "projectIds": [1],
                    "format": Format.XLSX,
                    "type": "translate",
                    "dateFrom": datetime(2023, 1, 1),
                    "dateTo": datetime(2023, 12, 31),
                    "groupBy": GroupBy.USER,
                    "typeTasks": 2,
                    "languageId": "uk",
                    "creatorId": 10,
                    "assigneeId": 20,
                    "wordsCountFrom": None,
                    "wordsCountTo": None,
                    "statuses": None,
                },
            ),
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.EnterpriseReportsResource.generate_group_report")
    def test_generate_group_task_usage_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = EnterpriseReportsResource(base_absolut_url)
        result = resource.generate_group_task_usage_report(group_id=1, **in_params)
        assert result == "response"

        m_generate_report.assert_called_once_with(
            group_id=1,
            request_data={"name": "group-task-usage", "schema": expected_schema},
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {},
                {
                    "projectIds": None,
                    "format": None,
                    "dateFrom": None,
                    "dateTo": None
                },
            ),
            (
                {
                    "project_ids": [1],
                    "format": Format.XLSX,
                    "date_from": datetime(2022, 5, 1),
                    "date_to": datetime(2022, 6, 1),
                },
                {
                    "projectIds": [1],
                    "format": Format.XLSX,
                    "dateFrom": datetime(2022, 5, 1),
                    "dateTo": datetime(2022, 6, 1),
                },
            ),
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.EnterpriseReportsResource.generate_group_report")
    def test_generate_group_qa_check_issues_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = EnterpriseReportsResource(base_absolut_url)
        result = resource.generate_group_qa_check_issues_report(group_id=1, **in_params)
        assert result == "response"

        m_generate_report.assert_called_once_with(
            group_id=1,
            request_data={"name": "group-qa-check-issues", "schema": expected_schema},
        )

    @pytest.mark.parametrize(
        "in_params, expected_schema",
        [
            (
                {
                    "unit": Unit.WORDS
                },
                {
                    "unit": Unit.WORDS,
                    "projectIds": None,
                    "format": None,
                    "dateFrom": None,
                    "dateTo": None,
                    "userIds": None,
                },
            ),
            (
                {
                    "unit": Unit.WORDS,
                    "project_ids": [1, 2, 3],
                    "format": Format.XLSX,
                    "date_from": datetime(2024, 1, 1),
                    "date_to": datetime(2024, 1, 31),
                },
                {
                    "unit": Unit.WORDS,
                    "projectIds": [1, 2, 3],
                    "format": Format.XLSX,
                    "dateFrom": datetime(2024, 1, 1),
                    "dateTo": datetime(2024, 1, 31),
                    "userIds": None,
                },
            ),
        ]
    )
    @mock.patch("crowdin_api.api_resources.reports.resource.EnterpriseReportsResource.generate_group_report")
    def test_generate_group_translation_activity_report(
            self, m_generate_report, in_params, expected_schema, base_absolut_url
    ):
        m_generate_report.return_value = "response"

        resource = EnterpriseReportsResource(base_absolut_url)
        result = resource.generate_group_translation_activity_report(group_id=1, **in_params)
        assert result == "response"
        m_generate_report.assert_called_once_with(
            group_id=1,
            request_data={"name": "group-translation-activity", "schema": expected_schema},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_report_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_report_generation_status(projectId=1, reportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_reports_path(projectId=1, reportId="hash")
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_report(projectId=1, reportId="hash") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_reports_path(projectId=1, reportId="hash") + "/download",
        )


class TestBaseReportSettingsTemplatesResource:
    resource_class = BaseReportSettingsTemplatesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"projectId": 1}, "projects/1/reports/settings-templates"),
            (
                {"projectId": 1, "reportSettingsTemplateId": 1},
                "projects/1/reports/settings-templates/1"
            ),
        ),
    )
    def test_get_reports_path(self, incoming_data, path, base_absolut_url):

        resource = self.get_resource(base_absolut_url)
        assert resource.get_report_settings_templates_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_report_settings_template(
        self,
        m_request,
        incoming_data,
        request_params,
        base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_report_settings_template(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_settings_templates_path(projectId=1),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "name": "test_name",
                    "currency": Currency.UAH,
                    "unit": Unit.WORDS,
                    "config": {
                        "regularRates": [
                            {
                                "mode": "tm_match",
                                "value": 0.1
                            }
                        ],
                        "individualRates": [
                            {
                                "languageIds": ["uk"],
                                "userIds": [1],
                                "rates": [
                                    {
                                        "mode": "tm_match",
                                        "value": 0.1
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "name": "test_name",
                    "currency": Currency.UAH,
                    "unit": Unit.WORDS,
                    "config": {
                        "regularRates": [
                            {
                                "mode": "tm_match",
                                "value": 0.1
                            }
                        ],
                        "individualRates": [
                            {
                                "languageIds": ["uk"],
                                "userIds": [1],
                                "rates": [
                                    {
                                        "mode": "tm_match",
                                        "value": 0.1
                                    }
                                ]
                            }
                        ]
                    },
                    "isPublic": None,
                    "isGlobal": None,
                },
            ),
            (
                {
                    "name": "test_name",
                    "currency": Currency.UAH,
                    "unit": Unit.WORDS,
                    "config": {
                        "regularRates": [
                            {
                                "mode": "tm_match",
                                "value": 0.1
                            }
                        ],
                        "individualRates": [
                            {
                                "languageIds": ["uk"],
                                "userIds": [1],
                                "rates": [
                                    {
                                        "mode": "tm_match",
                                        "value": 0.1
                                    }
                                ]
                            }
                        ]
                    },
                    "isPublic": False,
                },
                {
                    "name": "test_name",
                    "currency": Currency.UAH,
                    "unit": Unit.WORDS,
                    "config": {
                        "regularRates": [
                            {
                                "mode": "tm_match",
                                "value": 0.1
                            }
                        ],
                        "individualRates": [
                            {
                                "languageIds": ["uk"],
                                "userIds": [1],
                                "rates": [
                                    {
                                        "mode": "tm_match",
                                        "value": 0.1
                                    }
                                ]
                            }
                        ]
                    },
                    "isPublic": False,
                    "isGlobal": None,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_report_settings_template(
        self,
        m_request,
        incoming_data,
        request_data,
        base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_report_settings_template(projectId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_report_settings_templates_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        testing_result = resource.get_report_settings_template(
            projectId=1,
            reportSettingsTemplateId=1
        )
        assert testing_result == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_report_settings_templates_path(
                projectId=1,
                reportSettingsTemplateId=1
            )
        )

    @pytest.mark.parametrize(
        "value",
        [
            1,
            "test"
        ]
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_report_settings_template(self, m_request, base_absolut_url, value):
        m_request.return_value = "response"

        data = [
            {
                "value": value,
                "op": PatchOperation.REPLACE,
                "path": ReportSettingsTemplatesPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        testing_result = resource.edit_report_settings_template(
            projectId=1,
            reportSettingsTemplateId=1,
            data=data
        )
        assert testing_result == "response"
        m_request.assert_called_once_with(
            method="patch",
            request_data=data,
            path=resource.get_report_settings_templates_path(
                projectId=1,
                reportSettingsTemplateId=1
            )
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        testing_result = resource.delete_report_settings_template(
            projectId=1,
            reportSettingsTemplateId=1
        )
        assert testing_result == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_report_settings_templates_path(
                projectId=1,
                reportSettingsTemplateId=1
            )
        )


class TestUserReportSettingsTemplatesResource:
    resource_class = UserReportSettingsTemplatesResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"userId": 1}, "users/1/reports/settings-templates"),
            (
                {"userId": 1, "reportSettingsTemplateId": 1},
                "users/1/reports/settings-templates/1"
            ),
        ),
    )
    def test_get_user_report_settings_templates_path(
        self, incoming_data, path, base_absolut_url
    ):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_user_report_settings_templates_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            (
                {},
                {
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_user_report_settings_template(
        self,
        m_request,
        incoming_data,
        request_params,
        base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_user_report_settings_template(userId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_user_report_settings_templates_path(userId=1),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "incoming_data, request_data",
        (
            (
                {
                    "name": "test_name",
                    "currency": Currency.UAH,
                    "unit": Unit.WORDS,
                    "config": {
                        "regularRates": [
                            {
                                "mode": "tm_match",
                                "value": 0.1
                            }
                        ],
                        "individualRates": [
                            {
                                "languageIds": ["uk"],
                                "userIds": [1],
                                "rates": [
                                    {
                                        "mode": "tm_match",
                                        "value": 0.1
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "name": "test_name",
                    "currency": Currency.UAH,
                    "unit": Unit.WORDS,
                    "config": {
                        "regularRates": [
                            {
                                "mode": "tm_match",
                                "value": 0.1
                            }
                        ],
                        "individualRates": [
                            {
                                "languageIds": ["uk"],
                                "userIds": [1],
                                "rates": [
                                    {
                                        "mode": "tm_match",
                                        "value": 0.1
                                    }
                                ]
                            }
                        ]
                    }
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_user_report_settings_template(
        self,
        m_request,
        incoming_data,
        request_data,
        base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_user_report_settings_template(userId=1, **incoming_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_user_report_settings_templates_path(userId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_user_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_user_report_settings_template(
            userId=1,
            reportSettingsTemplateId=1
        ) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_user_report_settings_templates_path(
                userId=1,
                reportSettingsTemplateId=1
            ),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_user_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "value": "test",
                "op": PatchOperation.REPLACE,
                "path": ReportSettingsTemplatesPatchPath.NAME,
            }
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_user_report_settings_template(
            userId=1,
            reportSettingsTemplateId=1,
            data=data
        ) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_user_report_settings_templates_path(
                userId=1,
                reportSettingsTemplateId=1
            ),
            request_data=data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_user_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_user_report_settings_template(
            userId=1,
            reportSettingsTemplateId=1
        ) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_user_report_settings_templates_path(
                userId=1,
                reportSettingsTemplateId=1
            ),
        )


class TestReportsResourceNewReports:
    resource_class = ReportsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "name_method",
        [
            "list_user_report_settings_template",
            "add_user_report_settings_template",
            "get_user_report_settings_template",
            "edit_user_report_settings_template",
            "delete_user_report_settings_template",
        ],
    )
    def test_user_report_settings_templates_available(self, name_method):
        assert hasattr(ReportsResource, name_method)
        assert hasattr(EnterpriseReportsResource, name_method)

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_report_archives_filters(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        date_from = datetime(2024, 1, 1)
        date_to = datetime(2024, 2, 1)
        assert resource.list_report_archives(
            userId=1,
            taskId=2,
            name="archive",
            dateFrom=date_from,
            dateTo=date_to,
        ) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="users/1/reports/archives",
            params={
                "scopeType": None,
                "scopeId": None,
                "taskId": 2,
                "name": "archive",
                "dateFrom": date_from,
                "dateTo": date_to,
                "limit": 25,
                "offset": 0,
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_contribution_raw_data_by_task_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_contribution_raw_data_by_task_report(
            mode=ContributionMode.TRANSLATIONS,
            task_id=5,
            project_id=1,
            unit=Unit.WORDS,
            columns=["userId", "languageId"],
            tm_ids=[1],
            mt_ids=[2],
            ai_prompt_ids=[3],
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 2, 1),
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/reports",
            request_data={
                "name": "contribution-raw-data",
                "schema": {
                    "mode": ContributionMode.TRANSLATIONS,
                    "unit": Unit.WORDS,
                    "taskId": 5,
                    "columns": ["userId", "languageId"],
                    "tmIds": [1],
                    "mtIds": [2],
                    "aiPromptIds": [3],
                    "dateFrom": datetime(2024, 1, 1),
                    "dateTo": datetime(2024, 2, 1),
                },
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_translator_accuracy_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_translator_accuracy_report(
            project_id=1,
            unit=Unit.WORDS,
            format=Format.JSON,
            match_score_categories=["100-90"],
            language_id="uk",
            user_ids=[1],
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 2, 1),
            file_ids=[2],
            directory_ids=[3],
            branch_ids=[4],
            label_ids=[5],
            label_include_type=ReportLabelIncludeType.STRINGS_WITH_LABEL,
            skip_archiving=True,
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/reports",
            request_data={
                "name": "translator-accuracy",
                "schema": {
                    "unit": Unit.WORDS,
                    "format": Format.JSON,
                    "matchScoreCategories": ["100-90"],
                    "languageId": "uk",
                    "userIds": [1],
                    "dateFrom": datetime(2024, 1, 1),
                    "dateTo": datetime(2024, 2, 1),
                    "fileIds": [2],
                    "directoryIds": [3],
                    "branchIds": [4],
                    "labelIds": [5],
                    "labelIncludeType": ReportLabelIncludeType.STRINGS_WITH_LABEL,
                    "skipArchiving": True,
                },
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_time_spent_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_time_spent_report(
            project_id=1,
            format=Format.XLSX,
            group_by=GroupBy.TASK,
            base_rates={"hourly": 10.0},
            individual_rates=[{"languageIds": ["uk"], "userIds": [1], "hourly": 20.0}],
            language_id="uk",
            user_ids=[1],
            type_tasks=TaskType.PROOFREAD,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 2, 1),
            task_ids=[7],
            skip_archiving=False,
            workflow_step_id=9,
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/reports",
            request_data={
                "name": "time-spent",
                "schema": {
                    "format": Format.XLSX,
                    "groupBy": GroupBy.TASK,
                    "baseRates": {"hourly": 10.0},
                    "individualRates": [{"languageIds": ["uk"], "userIds": [1], "hourly": 20.0}],
                    "languageId": "uk",
                    "userIds": [1],
                    "typeTasks": TaskType.PROOFREAD,
                    "dateFrom": datetime(2024, 1, 1),
                    "dateTo": datetime(2024, 2, 1),
                    "taskIds": [7],
                    "workflowStepId": 9,
                    "skipArchiving": False,
                },
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_translation_activity_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_translation_activity_report(
            project_id=1,
            unit=Unit.WORDS,
            language_id="uk",
            format=Format.JSON,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 2, 1),
            user_ids=[1, 2],
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/reports",
            request_data={
                "name": "translation-activity",
                "schema": {
                    "unit": Unit.WORDS,
                    "languageId": "uk",
                    "format": Format.JSON,
                    "dateFrom": datetime(2024, 1, 1),
                    "dateTo": datetime(2024, 2, 1),
                    "userIds": [1, 2],
                },
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_report_settings_template_hourly(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        config = {
            "baseRates": {"hourly": 10.0},
            "individualRates": [{"languageIds": ["uk"], "userIds": [1], "hourly": 20.0}],
        }
        resource = self.get_resource(base_absolut_url)
        assert resource.add_report_settings_template(
            name="hourly",
            currency=Currency.PLN,
            unit=Unit.HOURS,
            config=config,
            projectId=1,
            isGlobal=True,
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/reports/settings-templates",
            request_data={
                "name": "hourly",
                "currency": Currency.PLN,
                "unit": Unit.HOURS,
                "config": config,
                "isPublic": None,
                "isGlobal": True,
            },
        )


class TestEnterpriseReportsResourceNewReports:
    resource_class = EnterpriseReportsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_report_archives_filters(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_report_archives(
            scopeType=ScopeType.GROUP,
            scopeId=1,
            userId=2,
            taskId=3,
            name="archive",
            dateFrom="2024-01-01",
            dateTo="2024-02-01",
        ) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="reports/archives",
            params={
                "scopeType": ScopeType.GROUP,
                "scopeId": 1,
                "userId": 2,
                "taskId": 3,
                "name": "archive",
                "dateFrom": "2024-01-01",
                "dateTo": "2024-02-01",
                "limit": 25,
                "offset": 0,
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_task_usage_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.generate_task_usage_report(
            project_id=1,
            format=Format.CSV,
            type=TaskUsageReportType.COST,
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 2, 1),
            group_by=GroupBy.TYPE,
            type_tasks=TaskType.TRANSLATE,
            language_id="uk",
            creator_id=1,
            assignee_id=2,
            words_count_from=10,
            words_count_to=20,
            statuses=[TaskUsageStatus.DONE],
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/reports",
            request_data={
                "name": "task-usage",
                "schema": {
                    "format": Format.CSV,
                    "type": TaskUsageReportType.COST,
                    "dateFrom": datetime(2024, 1, 1),
                    "dateTo": datetime(2024, 2, 1),
                    "groupBy": GroupBy.TYPE,
                    "typeTasks": TaskType.TRANSLATE,
                    "languageId": "uk",
                    "creatorId": 1,
                    "assigneeId": 2,
                    "wordsCountFrom": 10,
                    "wordsCountTo": 20,
                    "statuses": [TaskUsageStatus.DONE],
                },
            },
        )

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({"group_id": 1}, "groups/1/reports"),
            ({"group_id": 1, "report_id": "hash"}, "groups/1/reports/hash"),
        ),
    )
    def test_get_group_reports_path(self, incoming_data, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_group_reports_path(**incoming_data) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_group_report_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_group_report_generation_status(group_id=1, report_id="hash") == "response"
        m_request.assert_called_once_with(method="get", path="groups/1/reports/hash")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_group_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_group_report(group_id=1, report_id="hash") == "response"
        m_request.assert_called_once_with(method="get", path="groups/1/reports/hash/download")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_organization_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        request_data = {"name": "group-top-members", "schema": {}}
        assert resource.generate_organization_report(request_data=request_data) == "response"
        m_request.assert_called_once_with(method="post", path="reports", request_data=request_data)

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_check_organization_report_generation_status(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.check_organization_report_generation_status(report_id="hash") == "response"
        m_request.assert_called_once_with(method="get", path="reports/hash")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_download_organization_report(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.download_organization_report(report_id="hash") == "response"
        m_request.assert_called_once_with(method="get", path="reports/hash/download")

    @pytest.mark.parametrize(
        "method_name, in_params, name, schema",
        (
            (
                "generate_group_translation_costs_post_editing_general_report",
                {
                    "base_rates": "v_baseRates",
                    "individual_rates": "v_individualRates",
                    "net_rate_schemes": "v_netRateSchemes",
                    "project_ids": "v_projectIds",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "group_by": "v_groupBy",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "user_ids": "v_userIds",
                    "use_category_based_proofread_rates": "v_useCategoryBasedProofreadRates",
                    "use_tm_edit_distance": "v_useTmEditDistance",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-translation-costs-pe",
                {
                    "baseRates": "v_baseRates",
                    "individualRates": "v_individualRates",
                    "netRateSchemes": "v_netRateSchemes",
                    "projectIds": "v_projectIds",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "groupBy": "v_groupBy",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "userIds": "v_userIds",
                    "useCategoryBasedProofreadRates": "v_useCategoryBasedProofreadRates",
                    "useTmEditDistance": "v_useTmEditDistance",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_group_translation_costs_post_editing_by_task_report",
                {
                    "base_rates": "v_baseRates",
                    "individual_rates": "v_individualRates",
                    "net_rate_schemes": "v_netRateSchemes",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "task_ids": "v_taskIds",
                    "use_category_based_proofread_rates": "v_useCategoryBasedProofreadRates",
                    "use_tm_edit_distance": "v_useTmEditDistance",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-translation-costs-pe",
                {
                    "baseRates": "v_baseRates",
                    "individualRates": "v_individualRates",
                    "netRateSchemes": "v_netRateSchemes",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "taskIds": "v_taskIds",
                    "useCategoryBasedProofreadRates": "v_useCategoryBasedProofreadRates",
                    "useTmEditDistance": "v_useTmEditDistance",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_group_top_members_report",
                {
                    "project_ids": "v_projectIds",
                    "unit": "v_unit",
                    "language_id": "v_languageId",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "user_ids": "v_userIds",
                },
                "group-top-members",
                {
                    "projectIds": "v_projectIds",
                    "unit": "v_unit",
                    "languageId": "v_languageId",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "userIds": "v_userIds",
                },
            ),
            (
                "generate_group_task_usage_report",
                {
                    "format": "v_format",
                    "type": "v_type",
                    "project_ids": "v_projectIds",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "group_by": "v_groupBy",
                    "type_task": "v_typeTasks",
                    "language_id": "v_languageId",
                    "creator_id": "v_creatorId",
                    "assignee_id": "v_assigneeId",
                    "words_count_from": "v_wordsCountFrom",
                    "words_count_to": "v_wordsCountTo",
                    "statuses": "v_statuses",
                },
                "group-task-usage",
                {
                    "format": "v_format",
                    "type": "v_type",
                    "projectIds": "v_projectIds",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "groupBy": "v_groupBy",
                    "typeTasks": "v_typeTasks",
                    "languageId": "v_languageId",
                    "creatorId": "v_creatorId",
                    "assigneeId": "v_assigneeId",
                    "wordsCountFrom": "v_wordsCountFrom",
                    "wordsCountTo": "v_wordsCountTo",
                    "statuses": "v_statuses",
                },
            ),
            (
                "generate_group_qa_check_issues_report",
                {
                    "project_ids": "v_projectIds",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                },
                "group-qa-check-issues",
                {
                    "projectIds": "v_projectIds",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                },
            ),
            (
                "generate_group_translation_activity_report",
                {
                    "unit": "v_unit",
                    "project_ids": "v_projectIds",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "user_ids": "v_userIds",
                },
                "group-translation-activity",
                {
                    "unit": "v_unit",
                    "projectIds": "v_projectIds",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "userIds": "v_userIds",
                },
            ),
            (
                "generate_group_source_content_updates_report",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "project_ids": "v_projectIds",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                },
                "group-source-content-updates",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "projectIds": "v_projectIds",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                },
            ),
            (
                "generate_group_time_spent_report",
                {
                    "format": "v_format",
                    "group_by": "v_groupBy",
                    "base_rates": "v_baseRates",
                    "individual_rates": "v_individualRates",
                    "language_id": "v_languageId",
                    "user_ids": "v_userIds",
                    "type_tasks": "v_typeTasks",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "project_ids": "v_projectIds",
                    "task_ids": "v_taskIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-time-spent",
                {
                    "format": "v_format",
                    "groupBy": "v_groupBy",
                    "baseRates": "v_baseRates",
                    "individualRates": "v_individualRates",
                    "languageId": "v_languageId",
                    "userIds": "v_userIds",
                    "typeTasks": "v_typeTasks",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "projectIds": "v_projectIds",
                    "taskIds": "v_taskIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_group_pre_translate_accuracy_general_report",
                {
                    "unit": "v_unit",
                    "language_id": "v_languageId",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "match_score_categories": "v_matchScoreCategories",
                    "project_ids": "v_projectIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-pre-translate-accuracy",
                {
                    "unit": "v_unit",
                    "languageId": "v_languageId",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "matchScoreCategories": "v_matchScoreCategories",
                    "projectIds": "v_projectIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_group_pre_translate_accuracy_by_task_report",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "match_score_categories": "v_matchScoreCategories",
                    "task_ids": "v_taskIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-pre-translate-accuracy",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "matchScoreCategories": "v_matchScoreCategories",
                    "taskIds": "v_taskIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_group_translator_accuracy_report",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "language_id": "v_languageId",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "match_score_categories": "v_matchScoreCategories",
                    "user_ids": "v_userIds",
                    "project_ids": "v_projectIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-translator-accuracy",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "languageId": "v_languageId",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "matchScoreCategories": "v_matchScoreCategories",
                    "userIds": "v_userIds",
                    "projectIds": "v_projectIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_group_saving_activity_report",
                {
                    "unit": "v_unit",
                    "project_ids": "v_projectIds",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "language_id": "v_languageId",
                    "mode": "v_mode",
                },
                "group-saving-activity",
                {
                    "unit": "v_unit",
                    "projectIds": "v_projectIds",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "languageId": "v_languageId",
                    "mode": "v_mode",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_group_reports(
        self, m_request, method_name, in_params, name, schema, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert getattr(resource, method_name)(group_id=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="groups/1/reports",
            request_data={"name": name, "schema": schema},
        )

    @pytest.mark.parametrize(
        "method_name, in_params, name, schema",
        (
            (
                "generate_organization_translation_costs_post_editing_general_report",
                {
                    "base_rates": "v_baseRates",
                    "individual_rates": "v_individualRates",
                    "net_rate_schemes": "v_netRateSchemes",
                    "project_ids": "v_projectIds",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "group_by": "v_groupBy",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "user_ids": "v_userIds",
                    "use_category_based_proofread_rates": "v_useCategoryBasedProofreadRates",
                    "use_tm_edit_distance": "v_useTmEditDistance",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-translation-costs-pe",
                {
                    "baseRates": "v_baseRates",
                    "individualRates": "v_individualRates",
                    "netRateSchemes": "v_netRateSchemes",
                    "projectIds": "v_projectIds",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "groupBy": "v_groupBy",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "userIds": "v_userIds",
                    "useCategoryBasedProofreadRates": "v_useCategoryBasedProofreadRates",
                    "useTmEditDistance": "v_useTmEditDistance",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_organization_translation_costs_post_editing_by_task_report",
                {
                    "base_rates": "v_baseRates",
                    "individual_rates": "v_individualRates",
                    "net_rate_schemes": "v_netRateSchemes",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "task_ids": "v_taskIds",
                    "use_category_based_proofread_rates": "v_useCategoryBasedProofreadRates",
                    "use_tm_edit_distance": "v_useTmEditDistance",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-translation-costs-pe",
                {
                    "baseRates": "v_baseRates",
                    "individualRates": "v_individualRates",
                    "netRateSchemes": "v_netRateSchemes",
                    "unit": "v_unit",
                    "currency": "v_currency",
                    "format": "v_format",
                    "taskIds": "v_taskIds",
                    "useCategoryBasedProofreadRates": "v_useCategoryBasedProofreadRates",
                    "useTmEditDistance": "v_useTmEditDistance",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_organization_top_members_report",
                {
                    "project_ids": "v_projectIds",
                    "unit": "v_unit",
                    "language_id": "v_languageId",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "user_ids": "v_userIds",
                },
                "group-top-members",
                {
                    "projectIds": "v_projectIds",
                    "unit": "v_unit",
                    "languageId": "v_languageId",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "userIds": "v_userIds",
                },
            ),
            (
                "generate_organization_task_usage_report",
                {
                    "format": "v_format",
                    "type": "v_type",
                    "project_ids": "v_projectIds",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "group_by": "v_groupBy",
                    "type_tasks": "v_typeTasks",
                    "language_id": "v_languageId",
                    "creator_id": "v_creatorId",
                    "assignee_id": "v_assigneeId",
                    "words_count_from": "v_wordsCountFrom",
                    "words_count_to": "v_wordsCountTo",
                    "statuses": "v_statuses",
                },
                "group-task-usage",
                {
                    "format": "v_format",
                    "type": "v_type",
                    "projectIds": "v_projectIds",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "groupBy": "v_groupBy",
                    "typeTasks": "v_typeTasks",
                    "languageId": "v_languageId",
                    "creatorId": "v_creatorId",
                    "assigneeId": "v_assigneeId",
                    "wordsCountFrom": "v_wordsCountFrom",
                    "wordsCountTo": "v_wordsCountTo",
                    "statuses": "v_statuses",
                },
            ),
            (
                "generate_organization_qa_check_issues_report",
                {
                    "project_ids": "v_projectIds",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                },
                "group-qa-check-issues",
                {
                    "projectIds": "v_projectIds",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                },
            ),
            (
                "generate_organization_translation_activity_report",
                {
                    "unit": "v_unit",
                    "project_ids": "v_projectIds",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "user_ids": "v_userIds",
                },
                "group-translation-activity",
                {
                    "unit": "v_unit",
                    "projectIds": "v_projectIds",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "userIds": "v_userIds",
                },
            ),
            (
                "generate_organization_source_content_updates_report",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "project_ids": "v_projectIds",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                },
                "group-source-content-updates",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "projectIds": "v_projectIds",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                },
            ),
            (
                "generate_organization_time_spent_report",
                {
                    "format": "v_format",
                    "group_by": "v_groupBy",
                    "base_rates": "v_baseRates",
                    "individual_rates": "v_individualRates",
                    "language_id": "v_languageId",
                    "user_ids": "v_userIds",
                    "type_tasks": "v_typeTasks",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "project_ids": "v_projectIds",
                    "task_ids": "v_taskIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-time-spent",
                {
                    "format": "v_format",
                    "groupBy": "v_groupBy",
                    "baseRates": "v_baseRates",
                    "individualRates": "v_individualRates",
                    "languageId": "v_languageId",
                    "userIds": "v_userIds",
                    "typeTasks": "v_typeTasks",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "projectIds": "v_projectIds",
                    "taskIds": "v_taskIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_organization_pre_translate_accuracy_general_report",
                {
                    "unit": "v_unit",
                    "language_id": "v_languageId",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "match_score_categories": "v_matchScoreCategories",
                    "project_ids": "v_projectIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-pre-translate-accuracy",
                {
                    "unit": "v_unit",
                    "languageId": "v_languageId",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "matchScoreCategories": "v_matchScoreCategories",
                    "projectIds": "v_projectIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_organization_pre_translate_accuracy_by_task_report",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "match_score_categories": "v_matchScoreCategories",
                    "task_ids": "v_taskIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-pre-translate-accuracy",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "matchScoreCategories": "v_matchScoreCategories",
                    "taskIds": "v_taskIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_organization_translator_accuracy_report",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "language_id": "v_languageId",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "match_score_categories": "v_matchScoreCategories",
                    "user_ids": "v_userIds",
                    "project_ids": "v_projectIds",
                    "skip_archiving": "v_skipArchiving",
                },
                "group-translator-accuracy",
                {
                    "unit": "v_unit",
                    "format": "v_format",
                    "languageId": "v_languageId",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "matchScoreCategories": "v_matchScoreCategories",
                    "userIds": "v_userIds",
                    "projectIds": "v_projectIds",
                    "skipArchiving": "v_skipArchiving",
                },
            ),
            (
                "generate_organization_saving_activity_report",
                {
                    "unit": "v_unit",
                    "project_ids": "v_projectIds",
                    "format": "v_format",
                    "date_from": "v_dateFrom",
                    "date_to": "v_dateTo",
                    "language_id": "v_languageId",
                    "mode": "v_mode",
                },
                "group-saving-activity",
                {
                    "unit": "v_unit",
                    "projectIds": "v_projectIds",
                    "format": "v_format",
                    "dateFrom": "v_dateFrom",
                    "dateTo": "v_dateTo",
                    "languageId": "v_languageId",
                    "mode": "v_mode",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_generate_organization_reports(
        self, m_request, method_name, in_params, name, schema, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert getattr(resource, method_name)(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="reports",
            request_data={"name": name, "schema": schema},
        )

    @pytest.mark.parametrize(
        "incoming_data, path",
        (
            ({}, "reports/settings-templates"),
            ({"reportSettingsTemplateId": 1}, "reports/settings-templates/1"),
        ),
    )
    def test_get_organization_report_settings_templates_path(
        self, incoming_data, path, base_absolut_url
    ):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_organization_report_settings_templates_path(**incoming_data) == path

    @pytest.mark.parametrize(
        "incoming_data, request_params",
        (
            ({}, {"projectId": None, "groupId": None, "offset": 0, "limit": 25}),
            (
                {"project_id": 1, "group_id": 2, "offset": 5, "limit": 10},
                {"projectId": 1, "groupId": 2, "offset": 5, "limit": 10},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_organization_report_settings_templates(
        self, m_request, incoming_data, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_organization_report_settings_templates(**incoming_data) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="reports/settings-templates",
            params=request_params,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_organization_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        config = {
            "baseRates": {"fullTranslation": 0.1, "proofread": 0.05},
            "individualRates": [],
            "netRateSchemes": {"tmMatch": [], "mtMatch": [], "suggestionMatch": []},
        }
        resource = self.get_resource(base_absolut_url)
        assert resource.add_organization_report_settings_template(
            name="template",
            currency=Currency.USD,
            unit=Unit.WORDS,
            config=config,
            group_id=2,
            is_public=True,
        ) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="reports/settings-templates",
            request_data={
                "projectId": None,
                "groupId": 2,
                "name": "template",
                "currency": Currency.USD,
                "unit": Unit.WORDS,
                "config": config,
                "isPublic": True,
            },
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_organization_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_organization_report_settings_template(1) == "response"
        m_request.assert_called_once_with(method="get", path="reports/settings-templates/1")

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_organization_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        data = [
            {
                "op": PatchOperation.REPLACE,
                "path": ReportSettingsTemplatesPatchPath.IS_PUBLIC,
                "value": True,
            }
        ]
        resource = self.get_resource(base_absolut_url)
        assert resource.edit_organization_report_settings_template(1, data) == "response"
        m_request.assert_called_once_with(
            method="patch", path="reports/settings-templates/1", request_data=data
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_organization_report_settings_template(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_organization_report_settings_template(1) == "response"
        m_request.assert_called_once_with(method="delete", path="reports/settings-templates/1")

    @pytest.mark.parametrize(
        "method_name, kwargs, expected",
        (
            (
                "list_report_settings_template",
                {"projectId": 1},
                {
                    "method": "get",
                    "path": "projects/1/reports/settings-templates",
                    "params": {"offset": 0, "limit": 25},
                },
            ),
            (
                "add_report_settings_template",
                {
                    "name": "n",
                    "currency": Currency.USD,
                    "unit": Unit.WORDS,
                    "config": {},
                    "projectId": 1,
                },
                {
                    "method": "post",
                    "path": "projects/1/reports/settings-templates",
                    "request_data": {
                        "name": "n",
                        "currency": Currency.USD,
                        "unit": Unit.WORDS,
                        "config": {},
                        "isPublic": None,
                        "isGlobal": None,
                    },
                },
            ),
            (
                "get_report_settings_template",
                {"reportSettingsTemplateId": 2, "projectId": 1},
                {"method": "get", "path": "projects/1/reports/settings-templates/2"},
            ),
            (
                "edit_report_settings_template",
                {"reportSettingsTemplateId": 2, "data": [], "projectId": 1},
                {
                    "method": "patch",
                    "path": "projects/1/reports/settings-templates/2",
                    "request_data": [],
                },
            ),
            (
                "delete_report_settings_template",
                {"reportSettingsTemplateId": 2, "projectId": 1},
                {"method": "delete", "path": "projects/1/reports/settings-templates/2"},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_deprecated_project_report_settings_templates(
        self, m_request, method_name, kwargs, expected, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            assert getattr(resource, method_name)(**kwargs) == "response"
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)
        m_request.assert_called_once_with(**expected)
