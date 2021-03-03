from typing import List, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import ProjectPatchPath
from crowdin_api.typing import TypedDict


class ProjectPatchRequest(TypedDict):
    value: Union[str, List[str]]
    op: Union[PatchOperation, str]
    path: ProjectPatchPath
