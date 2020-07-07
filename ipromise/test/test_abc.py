# pylint: disable=unused-variable
from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass

from .common import HasAbstractMethod, HasRegularMethod, ImplementsAbstractMethod


class D:
    @abstractmethod
    def h(self) -> None:
        raise NotImplementedError


class A(AbstractBaseClass):
    def f(self) -> int:
        return 1

    @abstractmethod
    def g(self) -> None:
        raise NotImplementedError


class B(A):
    def f(self) -> int:
        return 2 + super().f()


class C(B):
    def g(self) -> None:
        pass


class E(C, D):
    pass


class AbstractHidesAbstractOkay(HasAbstractMethod):
    @abstractmethod
    def f(self) -> int:
        raise NotImplementedError


def test_unimplmented_abstract_methods() -> None:
    with pytest.raises(TypeError):
        A()  # type: ignore
    with pytest.raises(TypeError):
        B()  # type: ignore
        # Okay because it doesn't inherit from AbstractBaseClass:
        D()  # type: ignore


def test_implmented_abstract_methods() -> None:
    C()
    # Even though E.h is abstract, no promise is made because it was defined in a class D that
    # doesn't inherit from AbstractBaseClass.
    E()  # type: ignore


def test_abstractmethod_hiding() -> None:
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @abstractmethod
            def f(self) -> int:
                raise NotImplementedError


def test_abstractmethod_hiding_by_inheritance() -> None:
    with pytest.raises(TypeError):
        class Z(HasAbstractMethod, HasRegularMethod):
            pass


def test_abstractmethod_hiding_even_if_implemented() -> None:
    with pytest.raises(TypeError):
        class X(ImplementsAbstractMethod):
            @abstractmethod
            def f(self) -> int:
                raise NotImplementedError
