from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass, implements


class Z(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class A(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class B(A):

    @implements(A)
    def f(self):
        return 2 + super().f()


def test_implements():
    B()

    with pytest.raises(TypeError):
        # f in B is not abstract
        class C(A):
            @implements(B)
            def f(self):
                pass

    with pytest.raises(TypeError):
        # f is already implemented in base class B
        class C(B):
            @implements(A)
            def f(self):
                pass

    with pytest.raises(TypeError):
        class C(A):
            # Interface class Z is not a base class of C
            @implements(Z)
            def f(self):
                pass

    with pytest.raises(TypeError):
        class C(A):
            @implements(None)
            def f(self):
                pass

    with pytest.raises(TypeError):
        class C(A):
            # g not found in interace class A
            @implements(A)
            def g(self):
                pass
