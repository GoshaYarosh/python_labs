def to_json(obj):
    if not hasattr(obj, '__dict__'):
        return str(obj)

    json_string = '{ ';
    for name, value in obj.__dict__.iteritems():
        json_string += '{0}: {1}, '.format(name, to_json(value))
    json_string += ' }'
    return json_string

class A():
    pass
