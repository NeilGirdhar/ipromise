from typing import Any
from collections.abc import Callable

from .annotations import F

__all__ = ['overrides']


def overrides(interface_class: type[Any]) -> Callable[[F], F]:
    if not isinstance(interface_class, type):
        raise TypeError(
            f"interface class {interface_class} is not a type")

    def decorated_method(method: F) -> F:
        if hasattr(method, '__must_augment__'):
            raise TypeError(
                f"method {method.__name__} cannot be decorated with both "
                f"must_augment and overrides")
        if method.__name__ not in vars(interface_class):
            raise NotImplementedError(
                f"method {method.__name__} is an override but that "
                f"attribute is not implemented in interface class "
                f"{interface_class.__name__}")
        bases_value = getattr(interface_class, method.__name__)
        if not callable(bases_value):
            raise TypeError(
                f"method {method.__name__} is an override "
                f"but that is implemented as type {type(bases_value).__name__} "
                f"in base class {type(interface_class).__name__}, expected "
                f"override of a callable type")
        if hasattr(bases_value, '__overrides_from__'):
            raise TypeError(
                f"method {method.__name__} overrides a method in "
                f"the interface class {interface_class.__name__}, "
                f"but that method overrides from a higher-level interface "
                f"class {bases_value.__overrides_from__}")
        if getattr(bases_value, "__isabstractmethod__", False):
            raise TypeError(
                f"method {method.__name__} is abstract in interface class "
                f"{interface_class.__name__}")
        method.__overrides_from__ = interface_class  # type: ignore
        return method

    return decorated_method
