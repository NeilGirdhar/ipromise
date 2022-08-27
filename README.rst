#########
I Promise
#########

.. image:: https://badge.fury.io/py/ipromise.svg
    :target: https://badge.fury.io/py/ipromise
    :alt: ipromise badge

**I Promise** provides a Python base class, and decorators for
specifying promises relating to inheritance.

It provides three inheritance patterns:

* implementing,
* overriding, and
* augmenting.

Using the inheritance patterns can ensure an inheritance hierarchy
is used as intended by forcing a run-time failure when not.

----

.. contents::

----

**********
Installing
**********

.. code-block:: shell

    pip install ipromise

***
Use
***

Base class ``AbstractBaseClass``
================================

Checking promises depends on inheritance from the base class
``AbstractBaseClass``.  Unlike the standard library's similar class
``abc.ABCMeta``, the ``AbstractBaseClass`` does not bring in any metaclasses.
This is thanks to Python 3.6 `PEP 487
<https://peps.python.org/pep-0487/>`_
which added ``__init_subclass__``.

Implementing
============

*Implementing* is the pattern whereby an inheriting class's method implements an
abstract method from a base class method.

It is declared using the decorators:

* ``abc.abstractmethod`` from the standard library, and
* ``implements``, which indicates that a method implements an abstract method in
  a base class.

From ``samples/implements.py`` :

.. code-block:: python

    from ipromise import AbstractBaseClass, implements
    import abc

    class MyInterface(AbstractBaseClass):
        @abc.abstractmethod
        def f(self):
            raise NotImplementedError("You forgot to implement f()")

    class MyImplementation(MyInterface):
        @implements(MyInterface)
        def f(self):
            print("MyImplementation().f()")
            return 0

    MyImplementation().f()


Overriding
==========

*Overriding* is the pattern whereby an inheriting class's method replaces the
implementation of a base class method.
It is declared using the decorator ``overrides``, which marks the overriding
method.

An overriding method could call ``super`` but it is not required.

From ``samples/overrides.py`` :

.. code-block:: python

    from ipromise import AbstractBaseClass, overrides

    class MyClass(AbstractBaseClass):
        def f(self):
            print("MyClass().f()")
            return 1

    class MyClassButBetter(MyClass):
        @overrides(MyClass)
        def f(self):
            print("MyClassButBetter().f()")
            return 2

    MyClass().f()
    MyClassButBetter().f()

Augmenting
==========

*Augmenting* is a special case of *overriding* whereby the inheriting class's
method not only *overrides* the base class method, but *extends* its
functionality.
This means that it must delegate to *super* in all code paths.
This pattern is typical in multiple inheritance.

We hope that Python linters will be able to check for the super call.

Augmenting is declared using two decorators:

* ``augments`` indicates that this method must call super within its definition
  and thus augments the behavior of the base class method, and
* ``must_augment`` indicates that child classes that define this method must
  decorate their method overriddes with ``augments``.

From ``samples/augments.py`` :

.. code-block:: python

    from ipromise import AbstractBaseClass, must_augment, augments
    import abc

    class MyClass(AbstractBaseClass):
        @must_augment
        def f(self):
            # must_augment prevents this behavior from being lost.
            print("MyClass().f()")
            self.times_f_called += 1
            return 0

    class MyClassAgumentedOnce(MyClass):
        @augments(MyClass)
        def f(self, extra=0, **kwargs):
            print("MyClassAgumentedOnce().f()")
            return super().f(**kwargs) + extra

    class MyClassAgumentedOnceAgain(MyClassAgumentedOnce):
        @augments(MyClass)
        def f(self, **kwargs):
            print("MyClassAgumentedOnceAgain().f()")
            return super().f(**kwargs)

    MyClassAgumentedOnce().f()
    MyClassAgumentedOnceAgain().f()

***********
Development
***********

Pull Requests can be submitted on github.

poetry
======

The poetry development environment can be started with the typical
poetry commands:

.. code-block:: text

    poetry install
    poetry shell

Tools
=====

Tool commands should be run at the project top-level directory.

mypy
----

.. code-block:: text

    mypy ipromise test

flake8
------

.. code-block:: text

    pflake8 ipromise test

pytest
------

.. code-block:: text

    pytest -c pyproject.toml test

rst-lint
--------

Only necessary for ``README.rst`` changes.

.. code-block:: text

    rst-lint --level info README.rst
