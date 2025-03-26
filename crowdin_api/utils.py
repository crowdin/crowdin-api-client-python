from enum import Enum
from typing import Optional, Iterable, Callable


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
