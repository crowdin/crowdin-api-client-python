from typing import Any, Dict, Iterable, Optional, Union
from urllib.parse import quote

from deprecated import deprecated

from crowdin_api.api_resources.application.enums import IntegrationSyncProvider
from crowdin_api.api_resources.application.types import (
    AddApplicationConsentRequest,
    ApplicationConsentPatchRequest,
    ApplicationKVRecordPatchRequest,
    ApplicationManifest,
    ApplicationModulePermissions,
    ApplicationPermissions,
    ApplicationInstallationPatchRequest,
    IntegrationCrowdinUpdateFile,
    IntegrationSyncSettingsFile,
)
from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.sorting import Sorting


class ApplicationResource(BaseResource):
    """
    Crowdin Apps are web applications that can be integrated with Crowdin to extend its functionality.

    Use the API to manage the necessary app data.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Applications

    Link to documentation for enterprise:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Applications
    """

    def get_application_path(self, applicationIdentifier: str, path: str):
        return f"applications/{applicationIdentifier}/api/{path}"

    def get_application_installations_path(self, identifier: Optional[str] = None):
        if identifier:
            return f"applications/installations/{identifier}"
        return "applications/installations"

    def list_application_installations(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        installedBy: Optional[int] = None,
        orderBy: Optional[Sorting] = None,
    ):
        """
        List Application Installations

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.getMany
        """
        params = {"installedBy": installedBy, "orderBy": orderBy}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_application_installations_path(),
            params=params,
        )

    def install_application(
        self,
        url: Optional[str] = None,
        permissions: Optional[ApplicationPermissions] = None,
        manifest: Optional[ApplicationManifest] = None,
        modules: Optional[Iterable[ApplicationModulePermissions]] = None,
        assignAgent: Optional[bool] = None,
    ):
        """
        Install Application

        Install an application either from a hosted manifest URL (`url`) or from its
        manifest content (`manifest`, serverless apps only). Exactly one of `url` or
        `manifest` must be provided.

        `permissions.user` is deprecated by the API, use `modules` permissions instead.
        `assignAgent` is supported only when installing from a manifest URL.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.post
        """
        if (url is None) == (manifest is None):
            raise ValueError("You must set either url or manifest.")

        request_data = {
            "url": url,
            "manifest": manifest,
            "permissions": permissions,
            "modules": modules,
            "assignAgent": assignAgent,
        }
        return self.requester.request(
            method="post",
            path=self.get_application_installations_path(),
            request_data=request_data,
        )

    def get_application_installation(self, identifier: str):
        """
        Get Application Installation

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.get
        """
        return self.requester.request(
            method="get",
            path=self.get_application_installations_path(identifier=identifier),
        )

    def delete_application_installation(
        self, identifier: str, force: Optional[bool] = None
    ):
        """
        Delete Application Installation

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.delete

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.delete
        """
        params = {"force": force}

        return self.requester.request(
            method="delete",
            path=self.get_application_installations_path(identifier=identifier),
            params=params,
        )

    def edit_application_installation(
        self, identifier: str, data: Iterable[ApplicationInstallationPatchRequest]
    ):
        """
        Edit Application Installation

        Supported paths: `/permissions`, `/modules/{moduleKey}/permissions` and `/manifest`
        (the latter only for applications installed from manifest content).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_application_installations_path(identifier=identifier),
            request_data=data,
        )

    @deprecated("Use `edit_application_installation` instead")
    def edit_applicatoin_installation(
        self, identifier: str, data: Iterable[ApplicationInstallationPatchRequest]
    ):
        """
        Edit Application Installation

        Deprecated: use `edit_application_installation` instead.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.patch
        """
        return self.edit_application_installation(identifier=identifier, data=data)

    def upload_application_bundle(self, identifier: str, storageId: int):
        """
        Upload Application Bundle

        Upload a bundle archive (ZIP with a non-empty `app.js` at its root) for a
        serverless app installed from manifest content.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.bundles.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.bundles.post
        """
        return self.requester.request(
            method="post",
            path=f"{self.get_application_installations_path(identifier=identifier)}/bundles",
            request_data={"storageId": storageId},
        )

    def get_application_installation_update(self, identifier: str):
        """
        Get Application Installation Update

        Returns the diff between the installed application and the latest cached manifest,
        tagged with `manifestHash`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.update.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.update.get
        """
        return self.requester.request(
            method="get",
            path=f"{self.get_application_installations_path(identifier=identifier)}/update",
        )

    def apply_application_installation_update(self, identifier: str, manifestHash: str):
        """
        Apply Application Installation Update

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.installations.update.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.installations.update.post
        """
        return self.requester.request(
            method="post",
            path=f"{self.get_application_installations_path(identifier=identifier)}/update",
            request_data={"manifestHash": manifestHash},
        )

    def get_application_consents_path(self, consent_id: Optional[int] = None):
        if consent_id is not None:
            return f"applications/consents/{consent_id}"
        return "applications/consents"

    def list_application_consents(
        self,
        identifier: Optional[str] = None,
        order_by: Optional[Sorting] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Application Consents

        Available for Crowdin.com only (not supported in Crowdin Enterprise).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.consents.getMany
        """
        params = {
            "identifier": identifier,
            "orderBy": order_by,
        }
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self._get_entire_data(
            method="get",
            path=self.get_application_consents_path(),
            params=params,
        )

    def add_application_consent(self, request_data: AddApplicationConsentRequest):
        """
        Add Application Consent

        Available for Crowdin.com only (not supported in Crowdin Enterprise).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.consents.post
        """
        return self.requester.request(
            method="post",
            path=self.get_application_consents_path(),
            request_data=request_data,
        )

    def edit_application_consent(
        self,
        consent_id: int,
        request_data: Iterable[ApplicationConsentPatchRequest],
    ):
        """
        Edit Application Consent

        Available for Crowdin.com only (not supported in Crowdin Enterprise).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.consents.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_application_consents_path(consent_id=consent_id),
            request_data=request_data,
        )

    def delete_application_consent(self, consent_id: int):
        """
        Delete Application Consent

        Available for Crowdin.com only (not supported in Crowdin Enterprise).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.consents.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_application_consents_path(consent_id=consent_id),
        )

    def get_application_kv_records_path(
        self, applicationIdentifier: str, key: Optional[str] = None
    ):
        path = f"applications/{applicationIdentifier}/storage/kv/records"
        if key is not None:
            return f"{path}/{quote(key, safe='')}"
        return path

    def list_application_kv_records(
        self,
        applicationIdentifier: str,
        prefix: Optional[str] = None,
        orderBy: Optional[Sorting] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Application KV Records

        Requires the application's own access token (personal access tokens are not supported).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.storage.kv.records.getMany

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.storage.kv.records.getMany
        """
        params = {"prefix": prefix, "orderBy": orderBy}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_application_kv_records_path(applicationIdentifier),
            params=params,
        )

    def add_application_kv_record(
        self,
        applicationIdentifier: str,
        key: str,
        value: Any,
        secret: Optional[bool] = None,
        ttl: Optional[int] = None,
    ):
        """
        Add Application KV Record

        Requires the application's own access token (personal access tokens are not supported).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.storage.kv.records.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.storage.kv.records.post
        """
        return self.requester.request(
            method="post",
            path=self.get_application_kv_records_path(applicationIdentifier),
            request_data={"key": key, "value": value, "secret": secret, "ttl": ttl},
        )

    def get_application_kv_record(self, applicationIdentifier: str, key: str):
        """
        Get Application KV Record

        Requires the application's own access token (personal access tokens are not supported).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.storage.kv.records.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.storage.kv.records.get
        """
        return self.requester.request(
            method="get",
            path=self.get_application_kv_records_path(applicationIdentifier, key),
        )

    def edit_application_kv_record(
        self,
        applicationIdentifier: str,
        key: str,
        data: Iterable[ApplicationKVRecordPatchRequest],
    ):
        """
        Edit Application KV Record

        Requires the application's own access token (personal access tokens are not supported).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.storage.kv.records.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.storage.kv.records.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_application_kv_records_path(applicationIdentifier, key),
            request_data=data,
        )

    def delete_application_kv_record(self, applicationIdentifier: str, key: str):
        """
        Delete Application KV Record

        Requires the application's own access token (personal access tokens are not supported).

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.storage.kv.records.delete

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.storage.kv.records.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_application_kv_records_path(applicationIdentifier, key),
        )

    def get_application_data(
        self, applicationIdentifier: str, path: str, params: Optional[Dict] = None
    ):
        """
        Get Application Data.

        `params` are application-specific query parameters.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.api.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.api.get
        """

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, path),
            params=params,
        )

    def update_application_data(
        self, applicationIdentifier: str, path: str, data: dict, params: Optional[Dict] = None
    ):
        """
        Update or Restore Application Data.

        `params` are application-specific query parameters.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.api.put

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.api.put
        """

        return self.requester.request(
            method="put",
            path=self.get_application_path(applicationIdentifier, path),
            params=params,
            request_data=data,
        )

    def add_application_data(
        self, applicationIdentifier: str, path: str, data: dict, params: Optional[Dict] = None
    ):
        """
        Add Application Data.

        `params` are application-specific query parameters.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.api.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.api.post
        """

        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, path),
            params=params,
            request_data=data,
        )

    def delete_application_data(
        self, applicationIdentifier: str, path: str, params: Optional[Dict] = None
    ):
        """
        Delete Application Data.

        `params` are application-specific query parameters.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.api.delete

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.api.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_application_path(applicationIdentifier, path),
            params=params,
        )

    def edit_application_data(
        self, applicationIdentifier: str, path: str, data: dict, params: Optional[Dict] = None
    ):
        """
        Edit Application Data.

        `params` are application-specific query parameters.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.api.patch

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.api.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_application_path(applicationIdentifier, path),
            params=params,
            request_data=data,
        )

    # Integrations API (file-based projects only)

    def list_integration_crowdin_files(
        self, applicationIdentifier: str, projectId: Optional[int] = None
    ):
        """
        List Crowdin Files

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.crowdin.files

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.crowdin.files
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "crowdin-files"),
            params={"projectId": projectId},
        )

    def update_integration_crowdin_files(
        self,
        applicationIdentifier: str,
        files: Iterable[IntegrationCrowdinUpdateFile],
        uploadTranslations: Optional[bool] = None,
        projectId: Optional[int] = None,
    ):
        """
        Update Crowdin Files

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.crowdin.update

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.crowdin.update
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, "crowdin-update"),
            request_data={
                "projectId": projectId,
                "files": files,
                "uploadTranslations": uploadTranslations,
            },
        )

    def get_integration_file_progress(
        self, applicationIdentifier: str, fileId: int, projectId: Optional[int] = None
    ):
        """
        Get File Progress

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.file.progress

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.file.progress
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "file-progress"),
            params={"projectId": projectId, "fileId": fileId},
        )

    def get_integration_login_fields(self, applicationIdentifier: str):
        """
        Get Integration Login Form Fields

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.integration.fields

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.integration.fields
        """
        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "login-fields"),
        )

    def list_integration_files(
        self, applicationIdentifier: str, projectId: Optional[int] = None
    ):
        """
        List Integration Files

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.integration.files

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.integration.files
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "integration-files"),
            params={"projectId": projectId},
        )

    def integration_login(
        self,
        applicationIdentifier: str,
        credentials: Dict[str, Any],
        projectId: Optional[int] = None,
    ):
        """
        Integration Login

        `credentials` are the login form fields, see `get_integration_login_fields`.
        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.integration.login

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.integration.login
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, "login"),
            request_data={"projectId": projectId, "credentials": credentials},
        )

    def update_integration_files(
        self,
        applicationIdentifier: str,
        files: Dict[Union[int, str], Iterable[str]],
        projectId: Optional[int] = None,
    ):
        """
        Update Integration Files

        `files` maps Crowdin file ids to lists of language ids, e.g. `{102: ["de", "fr"]}`.
        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.integration.update

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.integration.update
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, "integration-update"),
            request_data={"projectId": projectId, "files": files},
        )

    def get_integration_job(
        self,
        applicationIdentifier: str,
        jobId: Optional[str] = None,
        projectId: Optional[int] = None,
    ):
        """
        Get Job

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.job.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.job.get
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "jobs"),
            params={"projectId": projectId, "jobId": jobId},
        )

    def cancel_integration_job(
        self, applicationIdentifier: str, jobId: str, projectId: Optional[int] = None
    ):
        """
        Cancel Job

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.job.cancel

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.job.cancel
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="delete",
            path=self.get_application_path(applicationIdentifier, "jobs"),
            params={"projectId": projectId, "jobId": jobId},
        )

    def get_integration_job_info(
        self, applicationIdentifier: str, jobId: str, projectId: Optional[int] = None
    ):
        """
        Get Job Info

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.job.info

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.job.info
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "job-info"),
            params={"projectId": projectId, "jobId": jobId},
        )

    def list_integration_jobs(
        self,
        applicationIdentifier: str,
        projectId: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Jobs

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.job.list

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.job.list
        """
        projectId = projectId or self.get_project_id()

        params = {"projectId": projectId}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_application_path(applicationIdentifier, "all-jobs"),
            params=params,
        )

    def get_integration_settings(
        self, applicationIdentifier: str, projectId: Optional[int] = None
    ):
        """
        Get Application Settings

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.settings.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.settings.get
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "settings"),
            params={"projectId": projectId},
        )

    def update_integration_settings(
        self,
        applicationIdentifier: str,
        config: Dict[str, Any],
        projectId: Optional[int] = None,
    ):
        """
        Update Application Settings

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.settings.update

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.settings.update
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, "settings"),
            request_data={"projectId": projectId, "config": config},
        )

    def get_integration_sync_settings(
        self,
        applicationIdentifier: str,
        provider: Union[IntegrationSyncProvider, str],
        projectId: Optional[int] = None,
    ):
        """
        Get Sync Settings

        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.sync.settings.get

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.sync.settings.get
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="get",
            path=self.get_application_path(applicationIdentifier, "sync-settings"),
            params={"projectId": projectId, "provider": provider},
        )

    def update_integration_sync_settings(
        self,
        applicationIdentifier: str,
        provider: IntegrationSyncProvider,
        files: Union[
            Dict[Union[int, str], Iterable[str]], Iterable[IntegrationSyncSettingsFile]
        ],
        projectId: Optional[int] = None,
    ):
        """
        Update Sync Settings

        `files` is either a mapping of Crowdin file ids to language ids
        (e.g. `{102: ["uk", "de"]}`) or a list of integration file objects.
        Available for file-based projects only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.applications.integrations.sync.settings.update

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.applications.integrations.sync.settings.update
        """
        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=self.get_application_path(applicationIdentifier, "sync-settings"),
            request_data={"projectId": projectId, "provider": provider, "files": files},
        )
