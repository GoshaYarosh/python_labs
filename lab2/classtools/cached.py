from functools import wraps


function_cache = dict()


def cached(function):
    function_cache[function] = dict()

    @wraps(function)
    def wrapper(*args, **kwargs):
        key = 'args: {0}, kwargs: {1}'.format(args, kwargs)
        current_cache = function_cache[function]
        if key not in current_cache:
            current_cache[key] = function(*args, **kwargs)
        return current_cache[key]

    return wrapper
