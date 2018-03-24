from .ipromise import AbstractBaseClass

__all__ = ['implements']


def implements(interface_class):

    if not isinstance(interface_class, type):
        raise TypeError

    def decorated_method(method):
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
        method.__implemented_from__ = interface_class
        return method

    return decorated_method
