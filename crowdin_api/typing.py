import sys

if sys.version_info >= (3, 8):
    pass
else:
    from typing_extensions import TypedDict  # noqa F401
