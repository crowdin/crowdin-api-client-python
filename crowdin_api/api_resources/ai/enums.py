from enum import Enum


class AIPromptAction(Enum):
    ASSIST = "assist"
    PRE_TRANSLATE = "pre_translate"


class EditAIPromptOperation(Enum):
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
