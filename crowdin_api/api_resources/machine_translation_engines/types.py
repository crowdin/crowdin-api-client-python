from typing import Any, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.machine_translation_engines.enums import (
    MachineTranslationEnginePatchPath,
)
from crowdin_api.typing import TypedDict


class MachineTranslationEngineApiKeyCredentials(TypedDict):
    """Google Translate, DeepL Pro and ModernMT credentials."""

    apiKey: str


class MachineTranslationEngineGoogleAutoMLCredentials(TypedDict):
    """Google AutoML Translate credentials (JSON file, base64 encoded)."""

    credentials: str


class MachineTranslationEngineMicrosoftCredentials(TypedDict, total=False):
    apiKey: str
    model: str


class MachineTranslationEngineAmazonCredentials(TypedDict):
    accessKey: str
    secretKey: str


class MachineTranslationEngineCustomMTCredentials(TypedDict):
    url: str


MachineTranslationEngineCredentials = Union[
    MachineTranslationEngineApiKeyCredentials,
    MachineTranslationEngineGoogleAutoMLCredentials,
    MachineTranslationEngineMicrosoftCredentials,
    MachineTranslationEngineAmazonCredentials,
    MachineTranslationEngineCustomMTCredentials,
]


class MachineTranslationEnginePatchRequest(TypedDict):
    op: PatchOperation
    path: MachineTranslationEnginePatchPath
    value: Any
