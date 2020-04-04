# pylint: disable=unused-variable
from abc import abstractmethod

import pytest

from ipromise import AbstractBaseClass, implements

from .common import HasAbstractMethod, ImplementsAbstractMethod


class AlsoHasAbstractMethod(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_implements_interface_is_not_a_base():
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(AlsoHasAbstractMethod)
            def f(self):
                pass


def test_is_already_implmented_in_base():
    with pytest.raises(TypeError):
        class X(ImplementsAbstractMethod):
            @implements(HasAbstractMethod)
            def f(self):
                pass


# Tests from implements.py.
# -----------------------------------------------------------------------------
def test_interface_is_not_a_type():
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(None)
            def f(self):
                pass


def test_implements_not_found_in_interface():
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(HasAbstractMethod)
            def g(self):
                pass


def test_implements_non_abstract_method():
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @implements(ImplementsAbstractMethod)
            def f(self):
                pass
