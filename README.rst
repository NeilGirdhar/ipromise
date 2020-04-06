=========
I Promise
=========
.. image:: https://badge.fury.io/py/ipromise.svg
    :target: https://badge.fury.io/py/ipromise

This repository provides a Python base class, and various decorators for specifying promises relating to inheritance.
It provides three inheritance patterns:

* implementing,
* overriding, and
* augmenting.

Base class
==========
Checking promises depends on inheritance from the base class ``AbstractBaseClass``.  Unlike the standard library's similar class ``abc.ABCMeta``, ``AbstractBaseClass`` does not bring in any metaclasses.  This is thanks to Python 3.6's PEP 487, which added ``__init_subclass__``.

Implementing
============
*Implementing* is the pattern whereby an inheriting class's method implements an abstract method from a base class method.
It is declared using the decorators:

* ``abc.abstractmethod`` from the standard library, and
* ``implements``, which indicates that a method implements an abstract method in a base class

For example:

.. code-block:: python

    class HasAbstractMethod(AbstractBaseClass):

        @abstractmethod
        def f(self):
            raise NotImplementedError


    class ImplementsAbstractMethod(HasAbstractMethod):

        @implements(HasAbstractMethod)
        def f(self):
            return 0

Overriding
==========
*Overriding* is the pattern whereby an inheriting class's method replaces the implementation of a base class method.
It is declared using the decorator ``overrides``, which marks the overriding method.

An overriding method could call super, but does not have to:

.. code-block:: python

    class HasRegularMethod(AbstractBaseClass):

        def f(self):
            return 1


    class OverridesRegularMethod(HasRegularMethod):

        @overrides(HasRegularMethod)
        def f(self):
            return 2

Augmenting
==========
*Augmenting* is a special case of *overriding* whereby the inheriting class's method not only *overrides* the base class method, but *extends* its functionality.
This means that it must delegate to *super* in all code paths.
This pattern is typical in multiple inheritance.

We hope that Python linters will be able to check for the super call.

Augmenting is declared using two decorators:

* ``augments`` indicates that this method must call super within its definition and thus augments the behavior of the base class method, and
* ``must_agugment`` indicates that child classes that define this method must decorate their method overriddes with ``augments``.

For example:

.. code-block:: python

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


    class AugmentsMethodFurther(AugmentsMethod):

        @augments(HasMustAugmentMethod)
        def f(self, **kwargs):
            print("f has been called")
            return super().f(**kwargs)
