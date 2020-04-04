# pylint: disable=unused-variable
from abc import abstractmethod

import pytest

from ipromise import AbstractBaseClass, implements, must_augment, overrides

from .common import (HasAbstractMethod, HasRegularMethod,
                     ImplementsAbstractMethod)


class OverridesRegularMethod(HasRegularMethod):

    @overrides(HasRegularMethod)
    def f(self):
        return 2


class OverridesImplementedAbstractMethod(ImplementsAbstractMethod):

    @overrides(ImplementsAbstractMethod)
    def f(self):
        return 1


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_overrides_from_other_class():
    with pytest.raises(TypeError):
        class X(AbstractBaseClass):
            @overrides(HasRegularMethod)
            def f(self):
                pass


def test_overrides_and_hides():
    class Y(AbstractBaseClass):
        def f(self):
            pass

    with pytest.raises(TypeError):
        class X(Y, HasRegularMethod):
            @overrides(HasRegularMethod)
            def f(self):
                return 1


def test_parent_overrides_different_method():
    class Y(HasRegularMethod):
        def f(self):
            pass

    class Z(Y):
        @overrides(Y)
        def f(self):
            pass

    with pytest.raises(TypeError):
        class X(Z, HasRegularMethod):
            @overrides(HasRegularMethod)
            def f(self):
                return 1


def test_parent_implements_different_method():
    class Y(AbstractBaseClass):
        @abstractmethod
        def f(self):
            raise NotImplementedError

    class Z(Y):
        @implements(Y)
        def f(self):
            pass

    with pytest.raises(TypeError):
        class X(Z, HasRegularMethod):
            @overrides(HasRegularMethod)
            def f(self):
                return 1


# Tests from overrides.py.
# -----------------------------------------------------------------------------
def test_interface_is_not_a_type():
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @overrides(None)
            def f(self):
                pass


def test_decorated_twice():
    with pytest.raises(TypeError):
        # Not found in interface class.
        class X(HasAbstractMethod):
            @overrides(HasRegularMethod)
            @must_augment
            def f(self):
                return 1


def test_not_found():
    with pytest.raises(TypeError):
        # Not found in interface class.
        class X(HasRegularMethod):
            @overrides(HasRegularMethod)
            def g(self):
                return 1


def test_override_an_override():
    with pytest.raises(TypeError):
        # Overrides an override.
        class X(OverridesImplementedAbstractMethod):
            @overrides(OverridesImplementedAbstractMethod)
            def f(self):
                return 1


def test_overrides_abstractmethod():
    with pytest.raises(TypeError):
        class X(ImplementsAbstractMethod):
            @overrides(HasAbstractMethod)
            def f(self):
                return 1
