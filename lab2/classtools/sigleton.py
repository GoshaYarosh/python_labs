class Singleton(object):
    """Sigleton class decorator

    Decorating some class makes it's object a sigleton. The first call of
    constructor will create instance of class and initialize it. Every other
    call of constructor will be returns the same instance.
    """

    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._cls.__new__(self._cls, *args, **kwargs)
            self._instance.__init__(*args, **kwargs)
        return self._instance
