from typing import Any, TypeVar
from collections.abc import Callable

__all__: list[str] = []


F = TypeVar('F', bound=Callable[..., Any])
Decorator = Callable[[F], F]  # Broken due to https://github.com/python/mypy/issues/8273.
