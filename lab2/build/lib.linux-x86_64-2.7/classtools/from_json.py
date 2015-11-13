import regex


# regular expressions for mathing json value types
_object_pattern = r'(?P<object>\{([^\}\{]*|(?&object))+\})'
_sequence_pattern = r'(?P<sequence>\[([^\]\[]*|(?&sequence))+\])'
_string_pattern = r'[\"].*?[\"]'
_int_pattern = r'[+-]?[\d]+'
_float_pattern = r'[+-]?[\d]+\.[\d]+'
_boolean_pattern = r'true|false'
_none_pattern = r'null'

# regular expression for math any json value
_value_pattern = r'(?P<value>' + '|'.join((
    _object_pattern,
    _sequence_pattern,
    _int_pattern,
    _float_pattern,
    _string_pattern,
    _boolean_pattern,
    _none_pattern
)) + ')'

# regular expression for match json key-value pair
_item_pattern = '(?P<key>{key}){delimiter}{value}'.format(
    delimiter=r'\s*:\s*',
    key=_string_pattern,
    value=_value_pattern
)


# converts json sequence into python list
def _parse_sequence(json_sequence):
    matches = regex.finditer(_value_pattern, json_sequence[1:-1])
    return [from_json(match.group('value')) for match in matches]


# converst json object into python object
def _parse_dict(json_object):
    matches = regex.finditer(_item_pattern, json_object[1: -1])
    dictionary = dict()
    for match in matches:
        # remove extra quotes from key
        key = match.group('key').lstrip('\'\"').rstrip('\'\"')
        value = from_json(match.group('value'))
        dictionary[key] = value
    return dictionary


# dictionary of patterns for json values and it converters in python objects
from_json_converters = {
    _object_pattern: _parse_dict,
    _sequence_pattern: _parse_sequence,
    _int_pattern: int,
    _float_pattern: float,
    _string_pattern: lambda json_str: json_str.lstrip('\"').rstrip('\"'),
    _boolean_pattern: lambda json_str: json_str == 'true',
    _none_pattern: lambda json_str: None,
}


def from_json(json_string):
    """From_json function

    Converts json object stored in string into python object:
        json object -> python dict
        json array -> python list
        json string -> python string
        json number -> python float or int
        json true or false -> python bool
        json null -> python None

    Usage:
        from_json('{"a": 1, "b": [1, 2, 3]}') -> {'a': 1, 'b': [1, 2, 3]}

    Exceptions:
        ValueError - json object has wrong syntax
    """

    for type_pattern, parse_func in from_json_converters.items():
        if regex.match(type_pattern, json_string, flags=regex.DOTALL):
            return parse_func(json_string)
    else:
        raise ValueError('Json syntax error')
