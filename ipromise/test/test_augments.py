# pylint: disable=unused-variable
from typing import Any

import pytest
from ipromise import AbstractBaseClass, augments, must_augment, overrides

from .common import HasAbstractMethod, HasRegularMethod


class HasMustAugmentMethod(AbstractBaseClass):

    def __init__(self) -> None:
        self.times_f_called = 0

    @must_augment
    def f(self) -> int:
        # must_augment prevents this behavior from being lost.
        self.times_f_called += 1
        return 0


class AugmentsMethod(HasMustAugmentMethod):

    @augments(HasMustAugmentMethod)
    def f(self, extra: int = 0, **kwargs: Any) -> int:
        # https://github.com/python/mypy/issues/4001
        return super().f(**kwargs) + extra  # type: ignore


class AlsoAugmentsMethod(HasMustAugmentMethod):

    @augments(HasMustAugmentMethod)
    def f(self, **kwargs: Any) -> int:
        print("f has been called")
        # https://github.com/python/mypy/issues/4001
        return super().f(**kwargs)  # type: ignore


class AugmentsRegularMethod(HasRegularMethod):
    @augments(HasRegularMethod)
    def f(self) -> int:
        return 1


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_must_agument_hides() -> None:
    class Y(AbstractBaseClass):
        def f(self) -> int:
            return 0

    with pytest.raises(TypeError):
        class X(HasMustAugmentMethod, Y):
            pass


# Tests from augments.py.
# -----------------------------------------------------------------------------
def test_decorated_twice_ma() -> None:
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @must_augment
            @augments(HasRegularMethod)
            def f(self) -> int:
                return 1


def test_decorated_twice_mo() -> None:
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @must_augment
            @overrides(HasRegularMethod)
            def f(self) -> int:
                return 1


def test_interface_is_not_a_type() -> None:
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @overrides(None)  # type: ignore
            def f(self) -> int:
                return 0


def test_decorated_twice_am() -> None:
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @augments(HasRegularMethod)
            @must_augment
            def f(self) -> int:
                return 1


def test_not_found() -> None:
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @augments(HasRegularMethod)
            def g(self) -> None:
                pass


def test_augments_an_augmented() -> None:
    with pytest.raises(TypeError):
        class X(AugmentsMethod):
            @augments(AugmentsMethod)
            def f(self, extra: int = 0, **kwargs: Any) -> int:
                return 1
