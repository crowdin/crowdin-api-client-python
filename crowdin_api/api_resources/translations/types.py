from typing import List, Optional

from crowdin_api.api_resources.translations.enums import CharTransformation
from crowdin_api.typing import TypedDict


class BuildRequest(TypedDict):
    branchId: Optional[int]
    targetLanguageIds: Optional[List[str]]
    skipUntranslatedStrings: Optional[bool]
    skipUntranslatedFiles: Optional[bool]
    exportApprovedOnly: Optional[bool]
    exportWithMinApprovalsCount: Optional[int]


class PseudoBuildRequest(TypedDict):
    pseudo: bool
    prefix: Optional[str]
    suffix: Optional[str]
    lengthTransformation: Optional[int]
    charTransformation: Optional[CharTransformation]
