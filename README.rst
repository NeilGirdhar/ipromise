====
ipromise
====
.. image:: https://badge.fury.io/py/ipromise.svg
    :target: https://badge.fury.io/py/ipromise

A Python base class that provides various decorators for specifying promises relating to inheritance.

It provides the decorator ``overridable``, which indicates that inheriting classes that define this method

- must decorate their method overriddes with ``overrides``, and
- must call super within their method definition::

    class A:

        @overridable
        def f(self):
            return 0


    class B(A):

        @overrides(A)
        def f(self):
            return super().f() + 1

It provides the decorator ``implements``, which indicates that a method
implements an abstract method in a base class::

    class A:

        @abstractmethod
        def f(self):
            raise NotImplementedError


    class B(A):

        @implements(A)
        def f(self):
            return 0
