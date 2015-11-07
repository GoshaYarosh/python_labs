from functools import wraps


# dict of functions caches
_function_caches = dict()


def cached(function):
    """cached function decorator

    Cache arguments and result of functions. Thereby function isn't called
    multiply times for the same arguments

    Arguments:
        function - a function that arguments and params will be cached
    """

    # dict for current function cache
    _function_caches[function] = dict()

    @wraps(function)
    def wrapper(*args, **kwargs):
        key = 'args: {0}, kwargs: {1}'.format(args, kwargs)
        current_function_cache = _function_caches[function]
        if key not in current_function_cache:
            current_function_cache[key] = function(*args, **kwargs)
        return current_function_cache[key]

    return wrapper
