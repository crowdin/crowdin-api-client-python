from unittest import mock

import pytest
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.application.resource import ApplicationResource
from crowdin_api.api_resources.application.enums import (
    ApplicationBundleMode,
    ApplicationConsentPatchPath,
    ApplicationConsentStatus,
    ApplicationInstallationPatchPath,
    ApplicationKVRecordPatchPath,
    ApplicationManifestEnvironment,
    IntegrationSyncProvider,
    ListApplicationConsentsOrderBy,
    UserPermissions,
    ProjectPermissions,
)
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestApplicationResource:
    resource_class = ApplicationResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"applicationIdentifier": "abc", "path": "test"}, "applications/abc/api/test"),
        ),
    )
    def test_get_applications_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, path",
        (
            (None, "applications/installations"),
            ("test", "applications/installations/test"),
        ),
    )
    def test_get_application_installation_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_installations_path(in_params) == path

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_application_installations(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_application_installations() == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_application_installations_path(),
            params={"installedBy": None, "orderBy": None, "offset": 0, "limit": 25},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_application_installations_with_filters(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        order_by = Sorting([SortingRule(ListApplicationConsentsOrderBy.ID, SortingOrder.ASC)])

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_application_installations(
                offset=5, limit=10, installedBy=12, orderBy=order_by
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_application_installations_path(),
            params={"installedBy": 12, "orderBy": order_by, "offset": 5, "limit": 10},
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "url": "https://localhost.dev/crowdin.json",
                },
                {
                    "url": "https://localhost.dev/crowdin.json",
                    "manifest": None,
                    "permissions": None,
                    "modules": None,
                    "assignAgent": None,
                }
            ),
            (
                {
                    "url": "https://localhost.dev/crowdin.json",
                    "permissions": {
                        "user": {
                            "value": UserPermissions.OWNER,
                            "ids": [1, 2, 3]
                        },
                        "project": {
                            "value": ProjectPermissions.OWN,
                            "ids": [4, 5, 6]
                        }
                    }
                },
                {
                    "url": "https://localhost.dev/crowdin.json",
                    "manifest": None,
                    "permissions": {
                        "user": {
                            "value": UserPermissions.OWNER,
                            "ids": [1, 2, 3]
                        },
                        "project": {
                            "value": ProjectPermissions.OWN,
                            "ids": [4, 5, 6]
                        }
                    },
                    "modules": None,
                    "assignAgent": None,
                }
            ),
            (
                {
                    "url": "https://localhost.dev/crowdin.json",
                    "modules": [
                        {
                            "key": "some-module-key",
                            "permissions": {
                                "user": {"value": UserPermissions.RESTRICTED, "ids": [1]}
                            },
                        }
                    ],
                    "assignAgent": True,
                },
                {
                    "url": "https://localhost.dev/crowdin.json",
                    "manifest": None,
                    "permissions": None,
                    "modules": [
                        {
                            "key": "some-module-key",
                            "permissions": {
                                "user": {"value": UserPermissions.RESTRICTED, "ids": [1]}
                            },
                        }
                    ],
                    "assignAgent": True,
                }
            ),
            (
                {
                    "manifest": {
                        "name": "My App",
                        "scopes": ["project"],
                        "modules": {
                            "project-tools": [
                                {
                                    "key": "my-module",
                                    "name": "My Module",
                                    "environments": [ApplicationManifestEnvironment.CROWDIN],
                                }
                            ]
                        },
                        "bundle": {"mode": ApplicationBundleMode.INTERNAL},
                    },
                    "permissions": {"project": {"value": ProjectPermissions.OWN, "ids": []}},
                },
                {
                    "url": None,
                    "manifest": {
                        "name": "My App",
                        "scopes": ["project"],
                        "modules": {
                            "project-tools": [
                                {
                                    "key": "my-module",
                                    "name": "My Module",
                                    "environments": [ApplicationManifestEnvironment.CROWDIN],
                                }
                            ]
                        },
                        "bundle": {"mode": ApplicationBundleMode.INTERNAL},
                    },
                    "permissions": {"project": {"value": ProjectPermissions.OWN, "ids": []}},
                    "modules": None,
                    "assignAgent": None,
                }
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_install_application(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.install_application(**in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_application_installations_path(),
            request_data=request_data
        )

    @pytest.mark.parametrize(
        "in_params",
        (
            {},
            {"url": "https://localhost.dev/crowdin.json", "manifest": {"name": "a", "modules": {}}},
        ),
    )
    def test_install_application_invalid(self, in_params, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        with pytest.raises(ValueError):
            resource.install_application(**in_params)

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_applcation_installation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        identifier = "example-application"
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_installation(identifier) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_application_installations_path(identifier),
        )

    @pytest.mark.parametrize(
        "in_params, request_param",
        (
            ({}, {"force": None}),
            ({"force": True}, {"force": True}),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_application_installation(
        self, m_request, in_params, request_param, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.delete_application_installation(
                identifier="example-app", **in_params
            )
            == "response"
        )
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_application_installations_path(identifier="example-app"),
            params=request_param
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_application_installation(
        self, m_request, base_absolut_url
    ):
        m_request.return_value = "response"

        identifier = "exmaple-application"
        data = [{"op": "replace", "path": "/permissions", "value": "test"}]
        resource = self.get_resource(base_absolut_url)
        assert resource.edit_application_installation(
            identifier=identifier,
            data=data,
        ) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_application_installations_path(identifier=identifier),
            request_data=data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_applicatoin_installation_deprecated(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        identifier = "exmaple-application"
        data = [
            {
                "op": PatchOperation.REPLACE,
                "path": ApplicationInstallationPatchPath.MANIFEST,
                "value": {"name": "My App", "modules": {}},
            }
        ]
        resource = self.get_resource(base_absolut_url)
        with pytest.deprecated_call():
            assert resource.edit_applicatoin_installation(
                identifier=identifier,
                data=data,
            ) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_application_installations_path(identifier=identifier),
            request_data=data,
        )

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({}, "applications/consents"),
            ({"consent_id": 12}, "applications/consents/12"),
        ),
    )
    def test_get_application_consents_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_consents_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {},
                {
                    "identifier": None,
                    "orderBy": None,
                    "limit": 25,
                    "offset": 0,
                },
            ),
            (
                {
                    "identifier": "example-application",
                    "order_by": Sorting(
                        [
                            SortingRule(
                                ListApplicationConsentsOrderBy.CREATED_AT,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "limit": 10,
                    "offset": 2,
                },
                {
                    "identifier": "example-application",
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListApplicationConsentsOrderBy.CREATED_AT,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "limit": 10,
                    "offset": 2,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_application_consents(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_application_consents(**in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_application_consents_path(),
            params=request_params,
        )

    @pytest.mark.parametrize(
        "request_data",
        (
            {
                "identifier": "example-application",
                "installedBy": 12,
                "status": ApplicationConsentStatus.GRANTED,
                "scopes": ["project", "tm"],
            },
            {
                "identifier": "example-application",
                "installedBy": 12,
                "status": ApplicationConsentStatus.DENIED,
                "scopes": None,
            },
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_application_consent(self, m_request, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_application_consent(request_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_application_consents_path(),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_application_consent(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        request_data = [
            {
                "op": PatchOperation.REPLACE,
                "path": ApplicationConsentPatchPath.STATUS,
                "value": ApplicationConsentStatus.DENIED,
            },
            {
                "op": PatchOperation.REPLACE,
                "path": ApplicationConsentPatchPath.SCOPES,
                "value": ["project"],
            },
        ]

        resource = self.get_resource(base_absolut_url)
        assert resource.edit_application_consent(12, request_data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_application_consents_path(consent_id=12),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_application_consent(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_application_consent(12) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_application_consents_path(consent_id=12),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_data(applicationIdentifier="abc", path="test") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
            params=None,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        # # assert resource.add_application_data(**in_params, request_data) == "response"
        dicts = {'key2': 2}
        assert resource.add_application_data("abc", "test", dicts) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
            params=None,
            request_data={"key2": 2},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_application_data(applicationIdentifier="abc", path="test") == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
            params=None,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        data = {"key2": 2}
        resource = self.get_resource(base_absolut_url)
        assert resource.edit_application_data(applicationIdentifier="abc", path="test", data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
            params=None,
            request_data={"key2": 2},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_update_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        data = {"key2": 2}
        resource = self.get_resource(base_absolut_url)
        assert resource.update_application_data(applicationIdentifier="abc", path="test", data=data) == "response"
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
            params=None,
            request_data={"key2": 2},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_application_data_with_params(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.get_application_data("abc", "test", params={"projectId": 1}) == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            path="applications/abc/api/test",
            params={"projectId": 1},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_upload_application_bundle(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.upload_application_bundle("example-app", storageId=12) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="applications/installations/example-app/bundles",
            request_data={"storageId": 12},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_application_installation_update(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_installation_update("example-app") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="applications/installations/example-app/update",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_apply_application_installation_update(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.apply_application_installation_update("example-app", manifestHash="abc")
            == "response"
        )
        m_request.assert_called_once_with(
            method="post",
            path="applications/installations/example-app/update",
            request_data={"manifestHash": "abc"},
        )

    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"applicationIdentifier": "app"}, "applications/app/storage/kv/records"),
            (
                {"applicationIdentifier": "app", "key": "user:1:settings"},
                "applications/app/storage/kv/records/user%3A1%3Asettings",
            ),
        ),
    )
    def test_get_application_kv_records_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_kv_records_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            ({}, {"prefix": None, "orderBy": None, "offset": 0, "limit": 25}),
            (
                {"prefix": "user:", "offset": 10, "limit": 5},
                {"prefix": "user:", "orderBy": None, "offset": 10, "limit": 5},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_application_kv_records(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.list_application_kv_records("app", **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            path="applications/app/storage/kv/records",
            params=request_params,
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {"key": "k", "value": {"a": 1}},
                {"key": "k", "value": {"a": 1}, "secret": None, "ttl": None},
            ),
            (
                {"key": "k", "value": "v", "secret": True, "ttl": 3600},
                {"key": "k", "value": "v", "secret": True, "ttl": 3600},
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_application_kv_record(
        self, m_request, in_params, request_data, base_absolut_url
    ):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.add_application_kv_record("app", **in_params) == "response"
        m_request.assert_called_once_with(
            method="post",
            path="applications/app/storage/kv/records",
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_application_kv_record(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_kv_record("app", "k") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="applications/app/storage/kv/records/k",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_application_kv_record(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        data = [
            {"op": PatchOperation.REPLACE, "path": ApplicationKVRecordPatchPath.VALUE, "value": 1},
            {"op": PatchOperation.REPLACE, "path": ApplicationKVRecordPatchPath.TTL, "value": 60},
        ]
        resource = self.get_resource(base_absolut_url)
        assert resource.edit_application_kv_record("app", "k", data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            path="applications/app/storage/kv/records/k",
            request_data=data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_application_kv_record(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.delete_application_kv_record("app", "k") == "response"
        m_request.assert_called_once_with(
            method="delete",
            path="applications/app/storage/kv/records/k",
        )

    @pytest.mark.parametrize(
        "method_name, in_params, http_method, api_path, call_kwargs",
        (
            (
                "list_integration_crowdin_files",
                {},
                "get",
                "crowdin-files",
                {"params": {"projectId": 1}},
            ),
            (
                "update_integration_crowdin_files",
                {"files": [{"id": "1", "name": "Landing pages"}], "uploadTranslations": True},
                "post",
                "crowdin-update",
                {
                    "request_data": {
                        "projectId": 1,
                        "files": [{"id": "1", "name": "Landing pages"}],
                        "uploadTranslations": True,
                    }
                },
            ),
            (
                "get_integration_file_progress",
                {"fileId": 2},
                "get",
                "file-progress",
                {"params": {"projectId": 1, "fileId": 2}},
            ),
            (
                "list_integration_files",
                {},
                "get",
                "integration-files",
                {"params": {"projectId": 1}},
            ),
            (
                "integration_login",
                {"credentials": {"email": "user@crowdin.com"}},
                "post",
                "login",
                {"request_data": {"projectId": 1, "credentials": {"email": "user@crowdin.com"}}},
            ),
            (
                "update_integration_files",
                {"files": {102: ["de", "fr"]}},
                "post",
                "integration-update",
                {"request_data": {"projectId": 1, "files": {102: ["de", "fr"]}}},
            ),
            (
                "get_integration_job",
                {"jobId": "j"},
                "get",
                "jobs",
                {"params": {"projectId": 1, "jobId": "j"}},
            ),
            (
                "cancel_integration_job",
                {"jobId": "j"},
                "delete",
                "jobs",
                {"params": {"projectId": 1, "jobId": "j"}},
            ),
            (
                "get_integration_job_info",
                {"jobId": "j"},
                "get",
                "job-info",
                {"params": {"projectId": 1, "jobId": "j"}},
            ),
            (
                "list_integration_jobs",
                {"offset": 0, "limit": 10},
                "get",
                "all-jobs",
                {"params": {"projectId": 1, "offset": 0, "limit": 10}},
            ),
            (
                "get_integration_settings",
                {},
                "get",
                "settings",
                {"params": {"projectId": 1}},
            ),
            (
                "update_integration_settings",
                {"config": {"schedule": "0"}},
                "post",
                "settings",
                {"request_data": {"projectId": 1, "config": {"schedule": "0"}}},
            ),
            (
                "get_integration_sync_settings",
                {"provider": IntegrationSyncProvider.CROWDIN},
                "get",
                "sync-settings",
                {"params": {"projectId": 1, "provider": IntegrationSyncProvider.CROWDIN}},
            ),
            (
                "update_integration_sync_settings",
                {"provider": IntegrationSyncProvider.INTEGRATION, "files": {102: ["uk"]}},
                "post",
                "sync-settings",
                {
                    "request_data": {
                        "projectId": 1,
                        "provider": IntegrationSyncProvider.INTEGRATION,
                        "files": {102: ["uk"]},
                    }
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_integration_methods(
        self, m_request, method_name, in_params, http_method, api_path, call_kwargs,
        base_absolut_url,
    ):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert getattr(resource, method_name)("app", projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method=http_method,
            path=f"applications/app/api/{api_path}",
            **call_kwargs,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_integration_methods_default_project(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=7
        )
        assert resource.list_integration_files("app") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="applications/app/api/integration-files",
            params={"projectId": 7},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_integration_login_fields(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.get_integration_login_fields("app") == "response"
        m_request.assert_called_once_with(
            method="get",
            path="applications/app/api/login-fields",
        )
