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
        bases_value = getattr(interface_class, method.__name__)
        # You are allowed to override abstract methods since a method can
        # be abstract and have a reasonable definition.  For example,
        # AbstractContextManager.__exit__.
#       if getattr(bases_value, "__isabstractmethod__", False):
#           raise TypeError(
#               f"{method.__name__} is abstract in interface class "
#               f"{interface_class.__name__}")
        method.__overrides_from__ = interface_class
        return method

    return decorated_method
