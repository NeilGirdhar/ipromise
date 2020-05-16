from typing import Any, Type, Callable

from .annotations import Decorator, F

__all__ = ['implements']


def implements(interface_class: Type[Any]) -> Callable[[F], F]:

    if not isinstance(interface_class, type):
        raise TypeError(
            f"interface class {interface_class} is not a type")

    def decorated_method(method: F) -> F:
        if method.__name__ not in vars(interface_class):
            raise TypeError(
                f"{method.__name__} not found in interface class "
                f"{interface_class.__name__}")
        if not getattr(getattr(interface_class, method.__name__),
                       "__isabstractmethod__",
                       False):
            raise TypeError(
                f"{method.__name__} in {interface_class.__name__} "
                "is not abstract")
        method.__implemented_from__ = interface_class  # type: ignore
        return method

    return decorated_method
