from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass, implements, overrides, overridable


class A(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class B(A):

    @overridable
    @implements(A)
    def f(self):
        return 0

class C(B):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class D(AbstractBaseClass):

    def f(self):
        return 1


class E(B):
    @overrides(B)
    def f(self):
        return 1


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_not_a_base_class():
    with pytest.raises(TypeError):
        class X(A):
            @overrides(B)
            def f(self):
                return 1

def test_somehow_abstract():
    # Somehow abstract in base class.
    class Y(C):
        @overrides(B)
        def f(self):
            return 1

def test_already_implemented():
    with pytest.raises(TypeError):
        # Already implemented in base class that does not inherit from B.
        class Z(B, D):
            @overrides(B)
            def f(self):
                return 1

# Tests from overrides.py.
# -----------------------------------------------------------------------------
def test_not_found():
    with pytest.raises(TypeError):
        # Not found in interface class.
        class V(B):
            @overrides(B)
            def g(self):
                return 1

def test_is_abstract():
    # Is abstract in interface class.
    class W(B):
        @overrides(B)
        def f(self):
            return 1

def test_override_an_override():
    with pytest.raises(TypeError):
        # Overrides an override.
        class U(E):
            @overrides(E)
            def f(self):
                return 1

def test_overrides_and_implemented():

    with pytest.raises(TypeError):
        class S(B):
            @overrides(A)
            def f(self):
                return 1

def test_overridable_despite_base_class():

    with pytest.raises(TypeError):
        class T(B):
            @overridable
            def f(self):
                return 1
