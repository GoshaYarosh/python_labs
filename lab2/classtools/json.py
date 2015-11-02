import types

_supported_types = (
    types.NoneType,
    types.ObjectType,
    types.StringType,
    types.IntType,
    types.FloatType,
    types.BooleanType,
    types.ListType,
    types.DictType
)


def to_json(obj):
    if hasattr(obj, '__dict__'):
        json_items = [
            "'{}': {}".format(attr, to_json(value))
            for (attr, value) in obj.__dict__.items()
            if type(value) in _supported_types and not attr.startswith('__')
        ]
        return '{' + ', '.join(json_items) + "}"
    else:
        return str(obj)


def from_json(json_string):
    obj = object()
    pass
