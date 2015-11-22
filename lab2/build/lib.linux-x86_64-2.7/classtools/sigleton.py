class Singleton(object):
    """Sigleton class decorator

    Decorating some class makes it's object a singleton. The first call of
    constructor will create instance of class and initialize it. Every other
    call of constructor will be returns the same instance.

    Usage:
        @Sigleton
        class SomeClass(object):
            pass
    """

    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    # calls on created new instance of decorated class
    def __call__(self, *args, **kwargs):
        if self._instance is None:
            # instance created first time
            self._instance = self._cls.__new__(self._cls, *args, **kwargs)
            self._instance.__init__(*args, **kwargs)
        return self._instance
