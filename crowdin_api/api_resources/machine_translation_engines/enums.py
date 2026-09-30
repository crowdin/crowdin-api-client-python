from enum import Enum


class LanguageRecognitionProvider(Enum):
    CROWDIN = "crowdin"
    ENGINE = "engine"


class MachineTranslationEngineType(Enum):
    GOOGLE = "google"
    GOOGLE_AUTOML = "google_automl"
    MICROSOFT = "microsoft"
    DEEPL = "deepl"
    AMAZON = "amazon"
    MODERNMT = "modernmt"
    CUSTOM_MT = "custom_mt"


class MachineTranslationEnginePatchPath(Enum):
    NAME = "/name"
    TYPE = "/type"
    CREDENTIALS = "/credentials"
    ENABLED_LANGUAGE_IDS = "/enabledLanguageIds"
    ENABLED_PROJECT_IDS = "/enabledProjectIds"
    IS_ENABLED = "/isEnabled"
