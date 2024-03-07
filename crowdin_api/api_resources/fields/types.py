from typing import Iterable, Any
from crowdin_api.typing import TypedDict
from crowdin_api.api_resources.fields.enums import (
    FieldPlace,
    FieldOperations,
    FieldsPatchPath,
)


class FieldOptions(TypedDict):
    label: str
    value: str


class FieldLocation(TypedDict):
    place: FieldPlace


class ListFieldConfig(TypedDict):
    options: Iterable[FieldOptions]
    locations: Iterable[FieldPlace]


class NumberFieldConfig(TypedDict):
    min: int
    max: int
    units: str
    locations: Iterable[FieldLocation]


class OtherFieldConfig(TypedDict):
    locations: Iterable[FieldLocation]


class FieldPatchRequest(TypedDict):
    op: FieldOperations
    path: FieldsPatchPath
    value: Any
