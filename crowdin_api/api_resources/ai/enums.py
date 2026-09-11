from enum import Enum


class AIPromptAction(Enum):
    PRE_TRANSLATE = "pre_translate"
    ALIGNMENT = "alignment"
    QA_CHECK = "qa_check"


class AIPromptOperation(Enum):
    REPLACE = "replace"
    TEST = "test"


class EditAIPromptPath(Enum):
    NAME = "/name"
    ACTION = "/action"
    AI_PROVIDER_ID = "/aiProviderId"
    AI_MODEL_ID = "/aiModelId"
    IS_ENABLED = "/isEnabled"
    ENABLED_PROJECT_IDS = "/enabledProjectIds"
    CONFIG = "/config"


class AIProviderType(Enum):
    OPEN_AI = "open_ai"
    AZURE_OPEN_AI = "azure_open_ai"
    GOOGLE_GEMINI = "google_gemini"
    MISTRAL_AI = "mistral_ai"
    ANTHROPIC = "anthropic"
    CUSTOM_AI = "custom_ai"


class EditAIProviderPath(Enum):
    NAME = "/name"
    TYPE = "/type"
    CREDENTIALS = "/credentials"
    CONFIG = "/config"
    IS_ENABLED = "/isEnabled"
    USE_SYSTEM_CREDENTIALS = "/useSystemCredentials"


class DatasetPurpose(Enum):
    TRAINING = "training"
    VALIDATION = "validation"


class EditAiCustomPlaceholderPatchPath(Enum):
    DESCRIPTION = "/description"
    PLACEHOLDER = "/placeholder"
    VALUE = "/value"


class AiPromptFineTuningJobStatus(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    CANCELED = "canceled"
    FAILED = "failed"
    FINISHED = "finished"


class AiToolType(Enum):
    FUNCTION = "function"


class AiReportType(Enum):
    TOKENS_USAGE_RAW_DATA = "tokens-usage-raw-data"


class EditAiSettingsPatchPath(Enum):
    EDITOR_SUGGESTION_AI_PROMPT_ID = "/editorSuggestionAiPromptId"
    SHORTCUTS = "/shortcuts"


class ListAiPromptFineTuningJobsOrderBy(Enum):
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    STARTED_AT = "startedAt"
    FINISHED_AT = "finishedAt"


class AiReportFormat(Enum):
    CSV = "csv"
    JSON = "json"


class ListSupportedAiModelsOrderBy(Enum):
    KNOWLEDGE_CUTOFF = "knowledgeCutoff"
    RELEASE_DATE = "releaseDate"


class AiRequestLogStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"


class AiRequestLogSourceAction(Enum):
    AI_PROXY = "ai_proxy"
    AI_GATEWAY = "ai_gateway"
    AI_TRANSLATE_STRINGS = "ai_translate_strings"
    AI_FILE_TRANSLATE = "ai_file_translate"
    AI_PROMPT_COMPLETION = "ai_prompt_completion"
    PRE_TRANSLATE_MANUAL = "pre_translate:manual"
    PRE_TRANSLATE_WORKFLOW = "pre_translate:workflow"
    AI_ALIGNMENT = "ai_alignment"
    QA_CHECK = "qa_check"
    AI_SUGGESTION = "ai_suggestion"
    ADVISOR = "advisor"
