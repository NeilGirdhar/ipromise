from abc import abstractmethod

import pytest

from ipromise import AbstractBaseClass

from .common import HasAbstractMethod, ImplementsAbstractMethod


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


def test_unimplmented_abstract_methods():
    with pytest.raises(TypeError):
        A()
    with pytest.raises(TypeError):
        B()
    D()  # Okay because it doesn't inherit from AbstractBaseClass.


def test_implmented_abstract_methods():
    C()
    E()


def test_abstractmethod_hiding():
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @abstractmethod
            def f(self):
                raise NotImplementedError


def test_abstractmethod_hiding_by_inheritance():
    class Y:
        @abstractmethod
        def f(self):
            raise NotImplementedError

    with pytest.raises(TypeError):
        class Z(Y, HasAbstractMethod):
            pass


def test_abstractmethod_hiding_even_if_implemented():
    with pytest.raises(TypeError):
        class X(ImplementsAbstractMethod):
            @abstractmethod
            def f(self):
                raise NotImplementedError
