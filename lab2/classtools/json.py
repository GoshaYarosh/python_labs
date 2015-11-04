# import types
import re

_object_pattern = r'\{.*?\}'
_sequence_pattern = r'\[.*?\]'
_string_pattern = r'[\"\'].*?[\"\']'
_int_pattern = r'[+-]?[\d]+'
_float_pattern = r'[+-]?[\d]+\.[\d]+'
_boolean_pattern = r'?i(true|false)'
_none_pattern = r'?inull'


_value_pattern = '|'.join((
    _object_pattern,
    _sequence_pattern,
    _int_pattern,
    _float_pattern,
    _string_pattern,
    _boolean_pattern,
    _none_pattern
))

_key_value_pair_pattern = '({key}){delimiter}({value})'.format(
    delimiter=r'\s*:\s*',
    key=_string_pattern,
    value=_value_pattern
)


def _parse_sequence(json_sequence):
    values = re.findall(_value_pattern, json_sequence[1:-1])
    return (from_json(value) for value in values)


def _parse_object(json_object):
    key_value_pairs = re.findall(
        _key_value_pair_pattern,
        json_object[1: -1]
    )
    obj = type('', (object, ), {})()
    for attr, value in key_value_pairs:
        setattr(obj, attr, from_json(value))
    return obj


from_json_converters = {
    _object_pattern: _parse_object,
    _sequence_pattern: _parse_sequence,
    _int_pattern: int,
    _float_pattern: float,
    _string_pattern: str,
    _boolean_pattern: lambda json_str: json_str == 'true',
    _none_pattern: lambda json_str: None,
}

# def _convert_object_to_json(obj):
#    json_values = ['"{}": {}'.]


# to_json_converters = {
#     types.ObjectType: ,
#     types.ListType: ,
#     types.StringType: str,
#     types.BooleanType: lambda obj: str(obj).lower(),
#     types.IntType: str,
#     types.FloatType: str,
#     types.NoneType: lambda obj: 'null'
# }

#
# def to_json(obj):
#     if hasattr(obj, '__dict__'):
#         json_items = [
#             "'{}': {}".format(attr, to_json(value))
#             for (attr, value) in obj.__dict__.items()
#             if type(value) in _supported_types and not attr.startswith('__')
#         ]
#         return '{' + ', '.join(json_items) + "}"
#     else:
#         return str(obj)


def from_json(json_string):
    for type_pattern, parse_func in from_json_converters.items():
        if re.match(type_pattern, json_string):
            return parse_func(json_string)
    else:
        raise ValueError('Json syntax error')
