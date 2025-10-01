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
    ReportLabelIncludeType
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
                    "dateTo": None
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
                },
            ),
        ]
    )

    @mock.patch("crowdin_api.api_resources.reports.resource.BaseReportsResource.generate_report")
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
                    "taskId": 1
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
                    "taskId": 1
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
                    "labelIncludeType": ReportLabelIncludeType.STRINGS_WITH_LABEL
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
                    "taskId": 1
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
                    "branchIds": [1]
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
                    "taskId": 1
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
                    "userIds": [10, 11]
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
                    "userIds": [10, 11]
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
                    "typeTask": None,
                    "languageId": None,
                    "creatorId": None,
                    "assigneeId": None,
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
                    "typeTask": 2,
                    "languageId": "uk",
                    "creatorId": 10,
                    "assigneeId": 20,
                },
            ),
        ]
    )

    @mock.patch("crowdin_api.api_resources.reports.resource.EnterpriseReportsResource.generate_group_report")
    def test_generate_group_task_usage_report(
            self,m_generate_report, in_params, expected_schema, base_absolut_url
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
            self,m_generate_report, in_params, expected_schema, base_absolut_url
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
                },
            ),
        ]
    )

    @mock.patch("crowdin_api.api_resources.reports.resource.EnterpriseReportsResource.generate_group_report")
    def test_generate_group_translation_activity_report(
            self, m_generate_report, in_params, expected_schema,base_absolut_url
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
                    "mode": "simple",
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
                    "mode": "simple",
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
                    "mode": "simple",
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
