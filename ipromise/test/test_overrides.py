from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass, implements, overrides


class A(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class B(A):

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

class W(A):
    @overrides(A)
    def f(self):
        return 1

def test_overrides():

    # Tests from ipromise.py.
    with pytest.raises(TypeError):
        # Not a base class.
        class X(A):
            @overrides(B)
            def f(self):
                return 1

    # Somehow abstract in base class.
    class Y(C):
        @overrides(B)
        def f(self):
            return 1

    with pytest.raises(TypeError):
        # Already implemented in base class that does not inherit from B.
        class Z(B, D):
            @overrides(B)
            def f(self):
                return 1

    # Tests from overrides.py.
    with pytest.raises(TypeError):
        # Not found in interface class.
        class V(A):
            @overrides(B)
            def g(self):
                return 1

    # Is abstract in interface class.
    class W(A):
        @overrides(A)
        def f(self):
            return 1
