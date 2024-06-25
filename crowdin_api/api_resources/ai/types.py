from typing import Any, Iterable, Optional, Union

from crowdin_api.api_resources.ai.enums import (
    AIPromptAction,
    EditAIPromptOperation,
    EditAIPromptPath,
)
from crowdin_api.typing import TypedDict


class OtherLanguageTranslation(TypedDict):
    isEnabled: Optional[bool]
    languageIds: Optional[Iterable[int]]


class BasicModePreTranslateActionCondfig(TypedDict):
    mode: str
    companyDescription: Optional[bool]
    projectDescription: Optional[bool]
    audienceDescription: Optional[bool]
    otherLanguageTranslation: Optional[OtherLanguageTranslation]
    glossaryTerms: Optional[bool]
    tmSuggestions: Optional[bool]
    fileContent: Optional[bool]
    fileContext: Optional[bool]
    publicProjectDescription: Optional[bool]


class BasicModeAssistActionCondfig(TypedDict):
    mode: str
    companyDescription: Optional[bool]
    projectDescription: Optional[bool]
    audienceDescription: Optional[bool]
    otherLanguageTranslation: Optional[OtherLanguageTranslation]
    glossaryTerms: Optional[bool]
    tmSuggestions: Optional[bool]
    fileContext: Optional[bool]
    publicProjectDescription: Optional[bool]
    siblingsStrings: Optional[bool]
    filteredStrings: Optional[bool]


class AdvancedModeConfig(TypedDict):
    mode: str
    prompt: str


class AddAIPromptRequestScheme(TypedDict):
    name: str
    action: AIPromptAction
    aiProviderId: int
    aiModelId: str
    isEnabled: Optional[bool]
    enabledProjectIds: Optional[Iterable[int]]
    config: Union[
        BasicModePreTranslateActionCondfig,
        BasicModeAssistActionCondfig,
        AdvancedModeConfig,
    ]


class EditAIPromptScheme(TypedDict):
    op: EditAIPromptOperation
    path: EditAIPromptPath
    value: Any
