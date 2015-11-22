class Field(object):

    def __init__(self, types, converter):
        self._types = types
        self._converter = converter

    def convert(self, value):
        if not issubclass(type(value), self._types):
            raise TypeError('Value type must be one of {}'.format(self._types))
        return self._converter(value)


class ObjectField(Field):

    def __init__(self, default_value=None):
        types = (object, )
        super(ObjectField, self).__init__(types, lambda value: value)


class IntField(Field):

    def __init__(self, default_value=None):
        types = (int, float, str)
        super(IntField, self).__init__(types, int)


class FloatField(Field):

    def __init__(self, default_value=None):
        types = (int, float, str)
        super(FloatField, self).__init__(types, float)


class StringField(Field):

    def __init__(self, default_value=None):
        types = (str, int, float, object)
        super(StringField, self).__init__(types, str)


class ModelCreator(type):
    '''ModelCreator metaclass

    Creates class with strong typed fields(type checking). Instance of class
    will has this fields with values specified in constructor

    Usage:
        class Person(object):
            __metaclass__ = ModelCreator
            name = StringField()
            age = IntField()

        person = Person(name='Jack', age=20)
    '''

    def __call__(cls, **kwargs):
        instance = cls.__new__(cls)
        instance.__init__()
        for attr_name, value in kwargs.items():
            if not hasattr(instance, attr_name):
                raise ValueError('Class {} hasnot attribute {}'.
                                 format(cls.__name__, attr_name))

            attr = getattr(instance, attr_name)
            if issubclass(type(attr), Field):
                setattr(instance, attr_name, attr.convert(value))
        return instance
