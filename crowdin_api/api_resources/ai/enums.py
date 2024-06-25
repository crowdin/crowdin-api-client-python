from enum import Enum


class AIPromptAction(Enum):
    ASSIST = "assist"
    PRE_TRANSLATE = "pre_translate"


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
    AZUER_OPEN_AI = "azure_open_ai"
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
