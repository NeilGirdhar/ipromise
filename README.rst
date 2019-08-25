========
ipromise
========

.. image:: https://badge.fury.io/py/ipromise.svg
    :target: https://badge.fury.io/py/ipromise

A Python base class that provides various decorators for specifying promises relating to inheritance.
It provides three inheritance patterns:

* implementing,
* augmenting, and
* overriding.

Implementing
============
Implementing is the pattern whereby an inheriting class's method implements an abstract method from a base class method.
It is declared using the decorators:

* ``abc.abstractmethod`` from the standard library, and
* ``implements``, which indicates that a method implements an abstract method in a base class

For example::

    class HasAbstractMethod(AbstractBaseClass):

        @abstractmethod
        def f(self):
            raise NotImplementedError


    class ImplementsAbstractMethod(HasAbstractMethod):

        @implements(HasAbstractMethod)
        def f(self):
            return 0

Augmenting
==========
Augmenting is the pattern whereby an inheriting class's method calls a base class method.
This pattern is typical in multiple inheritance whereby mixins provide additional behavior.
It is declared using two decorators:

* ``augments`` indicates that this method must call super within its definition and thus augments the behavior of the base class method, and
* ``must_agugment`` indicates that child classes that define this method must decorate their method overriddes with ``augments``.

For example::

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

Overriding
==========
Overriding is the pattern whereby an inheriting class's method calls a base class method.
This pattern indicates that the base class method is hidden (at least in some cases).
It is declared using the decorator ``overrides``, which indicates that this is an overriding method.
Such a method could call super, but does not have to::

    class HasRegularMethod(AbstractBaseClass):

        def f(self):
            return 1


    class OverridesRegularMethod(HasRegularMethod):

        @overrides(HasRegularMethod)
        def f(self):
            return 2
