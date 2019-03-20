# pylint: disable=unused-variable
from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass, implements, must_augment, overrides

from .common import HasAbstractMethod, HasRegularMethod, ImplementsAbstractMethod


class OverridesRegularMethod(HasRegularMethod):

    @overrides(HasRegularMethod)
    def f(self) -> int:
        return 2


class OverridesImplementedAbstractMethod(ImplementsAbstractMethod):

    @overrides(ImplementsAbstractMethod)
    def f(self) -> int:
        return 1


class AbstractBaseClassHasAbstractMethod(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class AbstractBaseClassHasNone(AbstractBaseClass):

    f = None


class AbstractBaseClassNoMethods(AbstractBaseClass):

    pass


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_overrides_from_other_class() -> None:
    with pytest.raises(TypeError):
        class X(AbstractBaseClass):
            @overrides(HasRegularMethod)
            def f(self) -> int:
                return 0


def test_overrides_and_hides() -> None:
    class Y(AbstractBaseClass):
        def f(self) -> int:
            return 0

    with pytest.raises(TypeError):
        class X(Y, HasRegularMethod):
            @overrides(HasRegularMethod)
            def f(self) -> int:
                return 1


def test_parent_overrides_different_method() -> None:
    class Y(HasRegularMethod):
        def f(self) -> int:
            pass

    class Z(Y):
        @overrides(Y)
        def f(self) -> int:
            pass

    with pytest.raises(TypeError):
        class X(Z, HasRegularMethod):
            @overrides(HasRegularMethod)
            def f(self) -> int:
                return 1


def test_parent_implements_different_method() -> None:
    class Y(AbstractBaseClass):
        @abstractmethod
        def f(self) -> int:
            raise NotImplementedError

    class Z(Y):
        @implements(Y)
        def f(self) -> int:
            return 0

    with pytest.raises(TypeError):
        class X(Z, HasRegularMethod):
            @overrides(HasRegularMethod)
            def f(self) -> int:
                return 1


# Tests from overrides.py.
# -----------------------------------------------------------------------------
def test_interface_is_not_a_type() -> None:
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @overrides(None)  # type: ignore
            def f(self) -> int:
                return 0


def test_decorated_twice() -> None:
    with pytest.raises(TypeError):
        # Not found in interface class.
        class X(HasAbstractMethod):
            @overrides(HasRegularMethod)
            @must_augment
            def f(self) -> int:
                return 1


def test_not_found() -> None:
    with pytest.raises(NotImplementedError):
        # Not found in interface class.
        class X(HasRegularMethod):
            @overrides(HasRegularMethod)
            def g(self) -> None:
                pass


def test_override_an_override() -> None:
    with pytest.raises(TypeError):
        # Overrides an override.
        class X(OverridesImplementedAbstractMethod):
            @overrides(OverridesImplementedAbstractMethod)
            def f(self) -> int:
                return 1


def test_overrides_abstractmethod() -> None:
    with pytest.raises(TypeError):
        class X(ImplementsAbstractMethod):
            @overrides(HasAbstractMethod)
            def f(self) -> int:
                return 1


def test_cannot_instantiate_abstract_class() -> None:
    # self test: TypeError … Can not instantiate abstract class …
    with pytest.raises(TypeError):
        AbstractBaseClassHasAbstractMethod()


def test_cannot_implements_overrides_of_abstractmethod() -> None:
    # TypeError method is abstract in interface class …
    with pytest.raises(TypeError):
        class X(AbstractBaseClassHasAbstractMethod):
            @implements(AbstractBaseClassHasAbstractMethod)
            @overrides(AbstractBaseClassHasAbstractMethod)
            def f(self):
                pass
        X()


def test_overrides_none_method_notimplementederror() -> None:
    # NotImplementedError … expected implemented type …
    with pytest.raises(NotImplementedError):
        class X(AbstractBaseClassHasNone):
            @overrides(AbstractBaseClassHasNone)
            def f(self):
                pass


def test_overrides_no_method_notimplementederror() -> None:
    # NotImplementedError … not implemented …
    with pytest.raises(NotImplementedError):
        class X(AbstractBaseClassNoMethods):
            @overrides(AbstractBaseClassNoMethods)
            def f(self):
                pass
