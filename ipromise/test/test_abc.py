from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass


class D:

    @abstractmethod
    def h(self):
        raise NotImplementedError


class A(AbstractBaseClass):

    def f(self):
        return 1

    @abstractmethod
    def g(self):
        raise NotImplementedError


class B(A):
    def f(self):
        return 2 + super().f()


class C(B):
    def g(self):
        pass


class E(C, D):
    pass


def test_abc():
    with pytest.raises(TypeError):
        A()
    with pytest.raises(TypeError):
        B()
    C()
    D()  # Okay because it doesn't inherit from AbstractBaseClass.
    E()
