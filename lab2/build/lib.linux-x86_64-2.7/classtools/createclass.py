from json import from_json


class CreateClass(type):
    '''CreateClass metaclass

    Creates class by class name, base classes and adds it attributes from file.
    Attributes in file should be stored in json format

    Usage:
        SomeClass = CreateClass('SomeClass', (object, ), 'attrs.json')
    '''

    def __new__(new_class, class_name, base_classes, args_file_name=None):
        new_class = type(class_name, base_classes, {})
        if args_file_name is not None:
            with open(args_file_name, 'r') as args_file:
                args_dict = from_json(args_file.read())
                for attr, value in args_dict.items():
                    setattr(new_class, attr, value)
        return new_class


if __name__ == '__main__':
    with open('popa.args', 'w') as args_file:
        args_file.write('{"a": 1, "b": [1, 2, 3], "c": 3}')

    Popa = CreateClass('Popa', (object, ), 'popa.args')
    print Popa.a, Popa.b, Popa.c
