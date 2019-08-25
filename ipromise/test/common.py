from abc import abstractmethod

from ipromise import AbstractBaseClass, implements


class HasAbstractMethod(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class ImplementsAbstractMethod(HasAbstractMethod):

    @implements(HasAbstractMethod)
    def f(self):
        return 0


class HasRegularMethod(AbstractBaseClass):

    def f(self):
        return 1
