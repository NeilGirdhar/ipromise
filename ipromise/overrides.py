from .ipromise import AbstractBaseClass

__all__ = ['overrides']


def overrides(interface_class):

    if not isinstance(interface_class, type):
        raise TypeError

    def decorated_method(method):
        if method.__name__ not in vars(interface_class):
            raise TypeError(
                f"{method.__name__} not found in interface class "
                f"{interface_class.__name__}")
        method.__overrides_from__ = interface_class
        return method

    return decorated_method
