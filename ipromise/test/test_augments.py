# pylint: disable=unused-variable
import pytest

from ipromise import AbstractBaseClass, augments, must_augment, overrides

from .common import HasAbstractMethod, HasRegularMethod


class HasMustAugmentMethod(AbstractBaseClass):

    @must_augment
    def f(self):
        # must_augment prevents this behavior from being lost.
        self.times_f_called += 1
        return 0


class AugmentsMethod(HasMustAugmentMethod):

    @augments(HasMustAugmentMethod)
    def f(self, extra=0, **kwargs):
        return super().f(**kwargs) + extra


class AlsoAugmentsMethod(HasMustAugmentMethod):

    @augments(HasMustAugmentMethod)
    def f(self, **kwargs):
        print("f has been called")
        return super().f(**kwargs)


class AugmentsRegularMethod(HasRegularMethod):
    @augments(HasRegularMethod)
    def f(self):
        return 1


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_must_agument_hides():
    class Y(AbstractBaseClass):
        def f(self):
            pass

    with pytest.raises(TypeError):
        class X(HasMustAugmentMethod, Y):
            pass


# Tests from augments.py.
# -----------------------------------------------------------------------------
def test_decorated_twice_ma():
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @must_augment
            @augments(HasRegularMethod)
            def f(self):
                return 1


def test_decorated_twice_mo():
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @must_augment
            @overrides(HasRegularMethod)
            def f(self):
                return 1


def test_interface_is_not_a_type():
    with pytest.raises(TypeError):
        class X(HasAbstractMethod):
            @overrides(None)
            def f(self):
                pass


def test_decorated_twice_am():
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @augments(HasRegularMethod)
            @must_augment
            def f(self):
                return 1


def test_not_found():
    with pytest.raises(TypeError):
        class X(HasRegularMethod):
            @augments(HasRegularMethod)
            def g(self):
                return 1


def test_augments_an_augmented():
    with pytest.raises(TypeError):
        class X(AugmentsMethod):
            @augments(AugmentsMethod)
            def f(self):
                return 1
