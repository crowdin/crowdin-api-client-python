from datetime import datetime
from unittest import mock

import pytest
from crowdin_api.api_resources.reports.enums import (
    ContributionMode,
    Currency,
    Format,
    GroupBy,
    SimpleRateMode,
    Unit,
)
from crowdin_api.api_resources.reports.resource import ReportsResource, EnterpriseReportsResource
from crowdin_api.requester import APIRequester


class TestReportsResource:
    resource_class = ReportsResource

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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
                    "format": None,
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
