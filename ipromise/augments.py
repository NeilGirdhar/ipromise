from .ipromise import AbstractBaseClass

__all__ = ['must_augment', 'augments']


def must_augment(method):
    if hasattr(method, '__augments_from__'):
        raise TypeError(
            f"{method.__name__} cannot be decorated both must_augment and "
            "augments")
    if hasattr(method, '__overrides_from__'):
        raise TypeError(
            f"{method.__name__} cannot be decorated both must_augment and "
            "overrides")
    method.__overridable__ = None
    return method


def augments(interface_class):
    if not isinstance(interface_class, type):
        raise TypeError

    def decorated_method(method):
        if hasattr(method, '__overridable__'):
            raise TypeError(
                f"{method.__name__} cannot be decorated both overridable and "
                "augments")
        if method.__name__ not in vars(interface_class):
            raise TypeError(
                f"{method.__name__} not found in interface class "
                f"{interface_class.__name__}")
        bases_value = getattr(interface_class, method.__name__)
        if hasattr(bases_value, '__augments_from__'):
            raise TypeError(
                f"the method {method.__name__} is augments a method in "
                f"the interface class {interface_class.__name__}, "
                f"but that method augments from a higher-level interface "
                f"class {getattr(bases_value, '__augments_from__')}")
#       if not hasattr(bases_value, '__overridable__'):
#           raise TypeError(
#               f"{method.__name__} is not decorated overridable in "
#               f"the interface class {interface_class.__name__}")
        # You are allowed to augment abstract methods since a method can
        # be abstract and have a reasonable definition.  For example,
        # AbstractContextManager.__exit__.
#       if getattr(bases_value, "__isabstractmethod__", False):
#           raise TypeError(
#               f"{method.__name__} is abstract in interface class "
#               f"{interface_class.__name__}")
        method.__augments_from__ = interface_class
        return method

    return decorated_method
