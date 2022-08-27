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


#MyInterface().f()  # raises TypeError
MyImplementation().f()
