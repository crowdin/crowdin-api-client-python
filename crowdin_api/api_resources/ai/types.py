from typing import Any, Dict, Iterable, Optional, Union

from crowdin_api.api_resources.ai.enums import (
    AIPromptAction,
    AIPromptOperation,
    AIProviderType,
    EditAIPromptPath,
    EditAIProviderPath,
    EditAiCustomPlaceholderPatchPath,
    AiToolType,
    EditAiSettingsPatchPath,
)
from crowdin_api.api_resources.enums import PatchOperation
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
    screenshots: Optional[bool]
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
    screenshots: Optional[bool]
    publicProjectDescription: Optional[bool]
    siblingsStrings: Optional[bool]
    filteredStrings: Optional[bool]


class AdvancedModeConfig(TypedDict):
    mode: str
    screenshots: Optional[bool]
    prompt: str


class ExternalMode(TypedDict):
    name: str
    identifier: str
    key: str
    options: Dict


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
        ExternalMode,
    ]


class EditAIPromptScheme(TypedDict):
    op: AIPromptOperation
    path: EditAIPromptPath
    value: Any


class OpenAICredential(TypedDict):
    apiKey: str


class AzureOpenAICredential(TypedDict):
    resourceName: str
    apiKey: str
    deploymentName: str
    apiVersion: str


class GoogleGeminiCredential(TypedDict):
    project: str
    region: str
    serviceAccountKey: Dict


class MistralAICredential(TypedDict):
    apiKey: str


class AnthropicCredential(TypedDict):
    apiKey: str


class CustomAICredential(TypedDict):
    identifier: str
    key: str


class ActionRule(TypedDict):
    action: AIPromptAction
    availableAiModelIds: Iterable[int]


class ActionRules(TypedDict):
    actionRules: Iterable[ActionRule]


class AddAIProviderReqeustScheme(TypedDict):
    name: str
    type: AIProviderType
    credentials: Optional[
        Union[
            OpenAICredential,
            AzureOpenAICredential,
            GoogleGeminiCredential,
            MistralAICredential,
            AnthropicCredential,
            CustomAICredential,
        ]
    ]
    config: Optional[ActionRules]
    isEnabled: Optional[bool]
    useSystemCredentials: Optional[bool]


class EditAIProviderRequestScheme(TypedDict):
    op: AIPromptOperation
    path: EditAIProviderPath
    value: Union[str, Dict, bool]


class GoogleGeminiChatProxy(TypedDict):
    model: str
    stream: Optional[bool]


class OtherChatProxy(TypedDict):
    stream: Optional[bool]


class GenerateAIPromptFineTuningDatasetRequest(TypedDict):
    projectIds: Optional[Iterable[int]]
    tmIds: Optional[Iterable[int]]
    purpose: Optional[str]
    dateFrom: str
    dateTo: str
    maxFileSize: Optional[int]
    minExamplesCount: Optional[int]
    maxExamplesCount: Optional[int]


class HyperParameters(TypedDict):
    batchSize: int
    learningRateMultiplier: float
    nEpochs: int


class TrainingOptions(TypedDict):
    projectIds: Optional[Iterable[int]]
    tmIds: Optional[Iterable[int]]
    dateFrom: Optional[str]
    dateTo: Optional[str]
    maxFileSize: Optional[int]
    minExamplesCount: Optional[int]
    maxExamplesCount: Optional[int]


class ValidationOptions(TypedDict):
    projectIds: Optional[Iterable[int]]
    tmIds: Optional[Iterable[int]]
    dateFrom: Optional[str]
    dateTo: Optional[str]
    maxFileSize: Optional[int]
    minExamplesCount: Optional[int]
    maxExamplesCount: Optional[int]


class CreateAIPromptFineTuningJobRequest(TypedDict):
    dryRun: Optional[bool]
    hyperparameters: Optional[HyperParameters]
    trainingOptions: TrainingOptions
    validationOptions: Optional[ValidationOptions]


class AddAiCustomPlaceholderRequest(TypedDict):
    description: str
    placeholder: str
    value: str


class EditAiCustomPlaceholderPatch(TypedDict):
    op: PatchOperation
    path: EditAiCustomPlaceholderPatchPath
    value: Any


class AiToolFunction(TypedDict):
    description: Optional[str]
    name: str
    parameters: Any


class AiTool(TypedDict):
    type: AiToolType
    function: AiToolFunction


class AiToolObject(TypedDict):
    tool: AiTool


class AiPromptContextResources(TypedDict):
    pass


class PreTranslateActionAiPromptContextResources(AiPromptContextResources):
    projectId: int
    sourceLanguageId: Optional[str]
    targetLanguageId: Optional[str]
    stringIds: Optional[Iterable[int]]
    overridePromptValues: Optional[Dict[str, str]]


class AssistActionAiPromptContextResources(AiPromptContextResources):
    projectId: int
    sourceLanguageId: Optional[str]
    targetLanguageId: Optional[str]
    stringIds: Optional[Iterable[int]]
    filteredStringIds: Optional[Iterable[int]]
    overridePromptValues: Optional[Dict[str, str]]


class QaCheckActionAiPromptContextResources(AiPromptContextResources):
    projectId: int
    sourceLanguageId: Optional[str]
    targetLanguageId: Optional[str]
    stringIds: Optional[Iterable[int]]
    overridePromptValues: Optional[Dict[str, str]]


class CustomActionAiPromptContextResources(AiPromptContextResources):
    projectId: int
    sourceLanguageId: Optional[str]
    targetLanguageId: Optional[str]
    stringIds: Optional[Iterable[int]]
    overridePromptValues: Optional[Dict[str, str]]
    customInstruction: Optional[str]


class GenerateAiPromptCompletionRequest(TypedDict):
    resources: AiPromptContextResources
    tools: Optional[Iterable[AiToolObject]]
    tool_choice: Any


class GeneralReportSchema(TypedDict):
    dateFrom: str
    dateTo: str
    format: Optional[str]
    projectIds: Optional[Iterable[int]]
    promptIds: Optional[Iterable[int]]
    userIds: Optional[Iterable[int]]


class GenerateAiReportRequest(TypedDict):
    type: str
    schema: GeneralReportSchema


class EditAiSettingsPatch(TypedDict):
    op: PatchOperation
    path: EditAiSettingsPatchPath
    value: Any
