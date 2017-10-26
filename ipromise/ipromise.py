__all__ = ['AbstractBaseClass', 'implements']


class AbstractBaseClass:

    def __init_subclass__(cls):
        super().__init_subclass__()

        # Assign the set of abstract method names to __abstractmethods__.
        # Python will not allow the class to be instantiated if this is not
        # empty.
        abstracts = {name
                     for name, value in vars(cls).items()
                     if getattr(value, "__isabstractmethod__", False)}
        for base in cls.__bases__:
            for name in getattr(base, "__abstractmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                    abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)

        # Check that all of the methods implementing pure virtual methods do
        # so.
        for name, value in vars(cls).items():
            if not hasattr(value, "__implemented_from__"):
                continue
            interface_class = getattr(value, "__implemented_from__")
            if not issubclass(cls, interface_class):
                raise TypeError(f"Interface class {interface_class.__name__} "
                                f"is not a base class of {cls.__name__}")
            for base in cls.__bases__:
                if not hasattr(base, name):
                    continue
                bases_value = getattr(base, name)
                if not getattr(bases_value, "__isabstractmethod__", False):
                    raise TypeError(f"{name} is already implemented "
                                    f"in base class {base.__name__}")


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
