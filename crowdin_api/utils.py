from enum import Enum
from typing import Any, Callable, Iterable, Optional


def convert_to_query_string(
    collection: Optional[Iterable],
    converter: Optional[Callable[[object], str]] = None
) -> Optional[str]:
    if not collection:
        return None

    if converter is not None:
        return ','.join(converter(item) for item in collection)
    else:
        return ','.join(str(item) for item in collection)


def convert_enum_to_string_if_exists(value: Optional[Enum]) -> Optional[str]:
    return value.value if value is not None else None


def convert_enum_collection_to_string_if_exists(value: Optional[Iterable[Enum]]) -> Optional[str]:
    if value is None:
        return None
    return ','.join([item.value for item in value if isinstance(item, Enum)])


def convert_to_query_list(value: Any) -> Any:
    """
    Serialize a query value that the API expects as a comma-separated list.

    Iterables (except strings) are joined with commas, using `.value` for enum members; an empty
    iterable becomes `None` so the filter is omitted. Single values are returned as they are.
    """
    if value is None or isinstance(value, (str, bytes, Enum)) or not isinstance(value, Iterable):
        return value

    items = list(value)
    if not items:
        return None

    return ",".join(str(item.value if isinstance(item, Enum) else item) for item in items)
