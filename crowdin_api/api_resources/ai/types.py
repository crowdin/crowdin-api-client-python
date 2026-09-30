from typing import Any, Dict, Iterable, Optional, Union

from crowdin_api.api_resources.ai.enums import (
    AIPromptAction,
    AIPromptOperation,
    AIProviderType,
    AiToolType,
    EditAiCustomPlaceholderPatchPath,
    EditAiSnippetPatchPath,
    EditAIPromptPath,
    EditAIProviderPath,
    EditAiSettingsPatchPath,
)
from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.typing import TypedDict


class OtherLanguageTranslation(TypedDict):
    isEnabled: Optional[bool]
    # Language identifiers, e.g. "uk", "de".
    languageIds: Optional[Iterable[Union[str, int]]]


class BasicModePreTranslateActionConfig(TypedDict):
    mode: str
    # Deprecated.
    companyDescription: Optional[Union[str, bool]]
    # Deprecated.
    projectDescription: Optional[Union[str, bool]]
    # Deprecated.
    audienceDescription: Optional[Union[str, bool]]
    # Deprecated: use `snippets` instead.
    customPlaceholders: Optional[Iterable[str]]
    snippets: Optional[Iterable[str]]
    # Deprecated: misspelled key, use `otherLanguageTranslations` instead.
    otherLanguageTranslation: Optional[OtherLanguageTranslation]
    otherLanguageTranslations: Optional[OtherLanguageTranslation]
    glossaryTerms: Optional[bool]
    tmSuggestions: Optional[bool]
    # Deprecated.
    fileContent: Optional[bool]
    fileContext: Optional[bool]
    generateFileSummary: Optional[bool]
    screenshots: Optional[bool]
    # Deprecated: use `projectContext` instead.
    publicProjectDescription: Optional[bool]
    projectContext: Optional[bool]
    # Crowdin Enterprise only.
    organizationContext: Optional[bool]
    siblingsStrings: Optional[bool]
    retryOnQaIssues: Optional[bool]


class BasicModeAlignmentActionConfig(TypedDict):
    mode: str
    # Deprecated.
    companyDescription: Optional[str]
    # Deprecated.
    projectDescription: Optional[str]
    # Deprecated.
    audienceDescription: Optional[str]
    # Deprecated: use `snippets` instead.
    customPlaceholders: Optional[Iterable[str]]
    snippets: Optional[Iterable[str]]
    # Deprecated: use `projectContext` instead.
    publicProjectDescription: Optional[bool]
    projectContext: Optional[bool]
    # Crowdin Enterprise only.
    organizationContext: Optional[bool]


class BasicModeQaCheckActionConfig(TypedDict):
    mode: str
    evaluationSteps: Iterable[str]
    # Deprecated: use `snippets` instead.
    customPlaceholders: Optional[Iterable[str]]
    snippets: Optional[Iterable[str]]
    glossaryTerms: Optional[bool]
    tmSuggestions: Optional[bool]
    fileContext: Optional[bool]
    screenshots: Optional[bool]
    # Deprecated: use `projectContext` instead.
    publicProjectDescription: Optional[bool]
    projectContext: Optional[bool]
    # Crowdin Enterprise only.
    organizationContext: Optional[bool]


class AdvancedModeConfig(TypedDict):
    mode: str
    generateFileSummary: Optional[bool]
    glossaryTerms: Optional[bool]
    tmSuggestions: Optional[bool]
    screenshots: Optional[bool]
    prompt: str
    otherLanguageTranslations: Optional[OtherLanguageTranslation]
    retryOnQaIssues: Optional[bool]


class ExternalMode(TypedDict):
    mode: str
    # Deprecated: not part of the API schema.
    name: str
    identifier: str
    key: str
    options: Dict
    retryOnQaIssues: Optional[bool]


class AddAIPromptRequestScheme(TypedDict):
    name: str
    action: AIPromptAction
    aiProviderId: int
    aiModelId: str
    # Deprecated.
    isEnabled: Optional[bool]
    enabledProjectIds: Optional[Iterable[int]]
    config: Union[
        BasicModePreTranslateActionConfig,
        BasicModeAlignmentActionConfig,
        BasicModeQaCheckActionConfig,
        AdvancedModeConfig,
        ExternalMode,
    ]


class EditAIPromptScheme(TypedDict):
    op: AIPromptOperation
    path: EditAIPromptPath
    value: Any


class OpenAICredential(TypedDict):
    apiKey: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class AzureOpenAICredential(TypedDict):
    resourceName: str
    apiKey: str
    deploymentName: str
    apiVersion: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class GoogleGeminiCredential(TypedDict):
    """Google Gemini (Vertex AI) credentials."""

    project: str
    region: str
    serviceAccountKey: Optional[Dict]
    workloadIdentityFederationAudience: Optional[str]
    serviceAccountEmail: Optional[str]
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class GoogleGeminiAIStudioCredential(TypedDict):
    apiKey: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class MistralAICredential(TypedDict):
    apiKey: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class AnthropicCredential(TypedDict):
    apiKey: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class XAICredential(TypedDict):
    apiKey: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class WatsonxCredential(TypedDict):
    apiKey: str
    projectId: str
    region: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class DeepSeekCredential(TypedDict):
    apiKey: str
    baseUrl: Optional[str]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class MicrosoftFoundryDeployment(TypedDict):
    deploymentName: str
    targetUri: str
    apiKey: str


class MicrosoftFoundryCredential(TypedDict):
    deployments: Iterable[MicrosoftFoundryDeployment]
    headers: Optional[Dict[str, str]]
    sendCustomHeadersOnly: Optional[bool]


class CustomAICredential(TypedDict):
    identifier: str
    key: str


class ActionRule(TypedDict):
    action: AIPromptAction
    availableAiModelIds: Iterable[Union[str, int]]


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
            GoogleGeminiAIStudioCredential,
            MistralAICredential,
            AnthropicCredential,
            XAICredential,
            WatsonxCredential,
            DeepSeekCredential,
            MicrosoftFoundryCredential,
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


class AddAiSnippetRequest(TypedDict):
    description: str
    placeholder: str
    value: str


class EditAiSnippetPatch(TypedDict):
    op: PatchOperation
    path: EditAiSnippetPatchPath
    value: Any


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
    projectDescription: Optional[str]


class AlignmentActionAiPromptContextResources(AiPromptContextResources):
    projectId: int
    sourceLanguageId: Optional[str]
    targetLanguageId: Optional[str]
    stringIds: Optional[Iterable[int]]
    overridePromptValues: Optional[Dict[str, str]]
    projectDescription: Optional[str]


class QaCheckActionAiPromptContextResources(AiPromptContextResources):
    projectId: int
    sourceLanguageId: Optional[str]
    targetLanguageId: Optional[str]
    stringIds: Optional[Iterable[int]]
    overridePromptValues: Optional[Dict[str, str]]
    projectDescription: Optional[str]


class CustomActionAiPromptContextResources(AiPromptContextResources):
    projectId: int
    sourceLanguageId: Optional[str]
    targetLanguageId: Optional[str]
    stringIds: Optional[Iterable[int]]
    overridePromptValues: Optional[Dict[str, str]]
    customInstruction: Optional[str]
    projectDescription: Optional[str]


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


class AiFileTranslationRequest(TypedDict):
    storageId: int
    targetLanguageId: str
    sourceLanguageId: Optional[str]
    type: Optional[str]
    parserVersion: Optional[int]
    tmIds: Optional[Iterable[int]]
    glossaryIds: Optional[Iterable[int]]
    styleGuideIds: Optional[Iterable[int]]
    aiPromptId: Optional[int]
    aiProviderId: Optional[int]
    aiModelId: Optional[str]
    instructions: Optional[Iterable[str]]
    attachmentIds: Optional[Iterable[int]]


class AiTranslateStringsRequest(TypedDict):
    strings: Iterable[str]
    targetLanguageId: str
    sourceLanguageId: Optional[str]
    tmIds: Optional[Iterable[int]]
    glossaryIds: Optional[Iterable[int]]
    styleGuideIds: Optional[Iterable[int]]
    aiPromptId: Optional[int]
    aiProviderId: Optional[int]
    aiModelId: Optional[str]
    instructions: Optional[Iterable[str]]
    attachmentIds: Optional[Iterable[int]]
