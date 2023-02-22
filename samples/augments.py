from ipromise import AbstractBaseClass, must_augment, augments


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


# MyClass().f()  # raises TypeError
MyClassAgumentedOnce().f()
MyClassAgumentedOnceAgain().f()
