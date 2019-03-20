========
ipromise
========

.. image:: https://badge.fury.io/py/ipromise.svg
    :target: https://badge.fury.io/py/ipromise

A Python base class that provides various decorators for specifying promises relating to inheritance.
It provides four method decorators:
* ``augments``,
* ``overrides``,
* ``implements``, and
* ``must_agugment``.

``must_agugment`` indicates that classes that define this method
must decorate their method overriddes with ``augments``.

``augments`` indicates that this method call super within its definition and thus augments the behavior of the base class method::

    class A:

        @must_augment  # This optional line prevents instantiation if this method is not augmented.
        def f(self):
            return 0


    class B(A):

        @augments(A)
        def f(self, extra=0, **kwargs):
            return super().f(**kwargs) + extra


    class C(A):

        @augments(A)
        def f(self, **kwargs):
            print("f has been called")
            return super().f(**kwargs)

This pattern is typical in multiple inheritance whereby many mixins can provide additional behavior.

``overrides`` indicates that this is an overriding method.  This pattern indicates that the base class method is hidden::

    class A:

        def f(self):
            return 0


    class B(A):

        @overrides(A)
        def f(self):
            return 23

``implements`` indicates that a method implements an abstract method in a base class::

    class A:

        @abstractmethod
        def f(self):
            raise NotImplementedError


    class B(A):

        @implements(A)
        def f(self):
            return 0
