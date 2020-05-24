# pylint: disable=unused-variable
from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass, implements

from .common import HasAbstractMethod, ImplementsAbstractMethod


class AlsoHasAbstractMethod(AbstractBaseClass):

    @abstractmethod
    def f(self) -> int:
        raise NotImplementedError


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_implements_interface_is_not_a_base() -> None:
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(AlsoHasAbstractMethod)
            def f(self) -> int:
                pass


def test_is_already_implmented_in_base() -> None:
    with pytest.raises(TypeError):
        class X(ImplementsAbstractMethod):
            @implements(HasAbstractMethod)
            def f(self) -> int:
                return 0


# Tests from implements.py.
# -----------------------------------------------------------------------------
def test_interface_is_not_a_type() -> None:
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(None)  # type: ignore
            def f(self) -> int:
                return 0


def test_implements_not_found_in_interface() -> None:
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(HasAbstractMethod)
            def g(self) -> None:
                pass


def test_implements_non_abstract_method() -> None:
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(ImplementsAbstractMethod)
            def f(self) -> int:
                return 0
