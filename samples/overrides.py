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
