__all__ = ['AbstractBaseClass']


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

        # Check that each method M implementing a method in class C:
        # * C is a base class, and
        # * overrides a virtual method.
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

        # Check that each method M overriding a method in class C:
        # * C is a base class, and
        # * overrides a non-virtual method.
        for name, value in vars(cls).items():
            if not hasattr(value, "__overrides_from__"):
                continue
            interface_class = getattr(value, "__overrides_from__")
            if not issubclass(cls, interface_class):
                raise TypeError(f"Interface class {interface_class.__name__} "
                                f"is not a base class of {cls.__name__}")
            for base in cls.__bases__:
                if not hasattr(base, name):
                    continue
                bases_value = getattr(base, name)
                if getattr(bases_value, "__isabstractmethod__", False):
                    raise TypeError(
                        f"{name} is abstract in base class {base.__name__}, "
                        f"so it should be marked as implemented rather than "
                        f"overridden.")
