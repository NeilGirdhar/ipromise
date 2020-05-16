from typing import Any, Callable, List, TypeVar

__all__: List[str] = []


F = TypeVar('F', bound=Callable[..., Any])
Decorator = Callable[[F], F]  # Broken due to https://github.com/python/mypy/issues/8273.
