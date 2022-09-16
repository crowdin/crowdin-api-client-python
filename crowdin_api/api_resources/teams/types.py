from typing import Iterable, Union

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.teams.enums import TeamPatchPath
from crowdin_api.typing import TypedDict


class TeamPatchRequest(TypedDict):
    value: Union[str, bool, Iterable[int], Iterable[dict]]
    op: PatchOperation
    path: TeamPatchPath


class It(TypedDict):
    workflowStepIds: Iterable[int]


class De(TypedDict):
    workflowStepIds: str


class Permissions(TypedDict):
    it: It
    de: De
