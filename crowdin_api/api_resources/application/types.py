from typing import Any, Dict, Iterable, Optional, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.application.enums import (
    ApplicationBundleMode,
    ApplicationConsentPatchPath,
    ApplicationConsentStatus,
    ApplicationInstallationPatchPath,
    ApplicationKVRecordPatchPath,
    ApplicationManifestEnvironment,
    UserPermissions,
    ProjectPermissions,
)


class ApplicationUser(TypedDict):
    value: UserPermissions
    ids: Iterable[int]


class ApplicationProject(TypedDict):
    value: ProjectPermissions
    ids: Iterable[int]


class ApplicationPermissions(TypedDict, total=False):
    user: ApplicationUser  # deprecated by the API, use module permissions instead
    project: ApplicationProject


class ApplicationModuleUserPermissions(TypedDict, total=False):
    user: ApplicationUser


class ApplicationModulePermissions(TypedDict, total=False):
    key: str
    permissions: ApplicationModuleUserPermissions


class _ApplicationManifestModuleRequired(TypedDict):
    key: str
    name: str


class ApplicationManifestModule(_ApplicationManifestModuleRequired, total=False):
    logo: str
    description: str
    environments: Iterable[ApplicationManifestEnvironment]
    permissions: ApplicationModuleUserPermissions


class ApplicationManifestDefaultPermissions(TypedDict, total=False):
    user: UserPermissions
    project: ProjectPermissions


class ApplicationManifestBundle(TypedDict, total=False):
    mode: ApplicationBundleMode
    url: str  # external mode only


class _ApplicationManifestRequired(TypedDict):
    name: str
    modules: Dict[str, Iterable[ApplicationManifestModule]]


class ApplicationManifest(_ApplicationManifestRequired, total=False):
    description: str
    logo: str
    scopes: Iterable[str]
    stringBasedAvailable: bool
    default_permissions: ApplicationManifestDefaultPermissions
    bundle: ApplicationManifestBundle


class ApplicationInstallationPatchRequest(TypedDict):
    op: Union[PatchOperation, str]
    path: Union[ApplicationInstallationPatchPath, str]
    value: Any


class AddApplicationConsentRequest(TypedDict):
    identifier: str
    installedBy: int
    status: ApplicationConsentStatus
    scopes: Optional[Iterable[str]]


class ApplicationConsentPatchRequest(TypedDict):
    op: PatchOperation
    path: ApplicationConsentPatchPath
    value: Any


class ApplicationKVRecordPatchRequest(TypedDict):
    op: PatchOperation
    path: ApplicationKVRecordPatchPath
    value: Any


class IntegrationCrowdinUpdateFile(TypedDict, total=False):
    id: str
    name: str
    parent_id: str
    parentId: str
    type: str
    node_type: str


class IntegrationSyncSettingsFile(TypedDict, total=False):
    id: str
    name: str
    parentId: str
    type: str
    node_type: str
    schedule: bool
