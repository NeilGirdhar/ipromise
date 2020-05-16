from abc import abstractmethod

from ipromise import AbstractBaseClass, implements


class HasAbstractMethod(AbstractBaseClass):

    @abstractmethod
    def f(self) -> int:
        raise NotImplementedError


class ImplementsAbstractMethod(HasAbstractMethod):

    @implements(HasAbstractMethod)
    def f(self) -> int:
        return 0


class HasRegularMethod(AbstractBaseClass):

    def f(self) -> int:
        return 1
