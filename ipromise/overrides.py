from typing import Any, Callable, Type

from .annotations import Decorator, F

__all__ = ['overrides']


def overrides(interface_class: Type[Any]) -> Callable[[F], F]:
    if not isinstance(interface_class, type):
        raise TypeError(
            f"interface class {interface_class} is not a type")

    def decorated_method(method: F) -> F:
        if hasattr(method, '__must_augment__'):
            raise TypeError(
                f"{method.__name__} cannot be decorated both must_augment and overrides")
        if method.__name__ not in vars(interface_class):
            raise NotImplementedError(
                f"method {method.__name__} is an @overrides but that "
                f"method is not implemented in interface class "
                f"{interface_class.__name__}")
        def func():
            pass
        bases_value = getattr(interface_class, method.__name__)
        if type(bases_value) is not type(func):
            raise NotImplementedError(
                f"method {method.__name__} is an @overrides "
                f"but that is implemented as type {type(bases_value)} "
                f"in base class {interface_class}, expected implemented "
                f"type {type(func)}")
        if hasattr(bases_value, '__overrides_from__'):
            raise TypeError(
                f"The method {method.__name__} @overrides a method in "
                f"the interface class {interface_class.__name__}, "
                f"but that method @overrides from a higher-level interface "
                f"class {getattr(bases_value, '__overrides_from__')}")
        if getattr(bases_value, "__isabstractmethod__", False):
            raise TypeError(
                f"the method {method.__name__} is abstract in interface class "
                f"{interface_class.__name__}")
        method.__overrides_from__ = interface_class  # type: ignore
        return method

    return decorated_method
