from typing import Any

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import ProjectPatchPath
from crowdin_api.typing import TypedDict


class ProjectPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: ProjectPatchPath


class NotificationSettings(TypedDict):
    translatorNewStrings: bool
    managerNewStrings: bool
    managerLanguageCompleted: bool


class QACheckCategories(TypedDict):
    EMPTY: bool
    SIZE: bool
    TAGS: bool
    SPACES: bool
    VARIABLES: bool
    PUNCTUATION: bool
    SYMBOLREGISTER: bool
    SPECIALSYMBOLS: bool
    WRONGTRANSLATION: bool
    SPELLCHECK: bool
    ICU: bool
    TERMS: bool
    DUPLICATE: bool
