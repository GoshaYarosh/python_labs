import types


# converts some python object to json
def _dict_to_json(dictionary):
    json_items = [
        '"{}": {}'.format(str(key), to_json(value))
        for key, value in dictionary.items()
    ]
    return '{' + ', '.join(json_items) + '}'


# converts python list or tuple to json sequence
def _sequence_to_json(sequence):
    json_sequence = ', '.join(
        to_json(value) for value in sequence
    )
    return '[' + json_sequence + ']'


# dictionary of python types and it json converters
to_json_converters = {
    types.DictType: _dict_to_json,
    types.ListType: _sequence_to_json,
    types.StringType: lambda string: '"' + string + '"',
    types.BooleanType: lambda obj: str(obj).lower(),
    types.IntType: str,
    types.FloatType: str,
    types.NoneType: lambda obj: 'null'
}


def to_json(obj):
    '''to_json function

    Converts some python object in json object:
        python object or dict -> json object
        python int, long, float -> json number
        python list, tuple -> json array
        python bool -> json true or false
        python None -> json null

    Usage:
        to_json({'a': 1, 'b': [1, 2, 3]}) -> '{"a": 1, "b": [1, 2, 3]}'
    '''

    if type(obj) in to_json_converters:
        converter = to_json_converters[type(obj)]
        return converter(obj)
    else:
        raise TypeError('Unsupported type: {0}'.format(type(obj)))
