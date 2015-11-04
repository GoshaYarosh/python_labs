from functools import wraps


class Logger(object):
    '''Logger class.
    Log information about calls of all instance methods of object of class:
    method name, positional and named arguments, method result.
    You can specify the format string of calls logging. Info will be stored

    into this keyword arguments:
        method_name - the name of the called method
        args - positional arguments passed to the method
        kwargs - named arguments passed to the method
        result - result of execution of the method

    Methods:
        log_method(method) - method that decorates calls of all instance methods
        __init__(log_format) - specification of the format string for calls
        __str__() - returns string representation of the log
    '''

    # default format string for call logging
    default_log_format = ''.join((
        'Method: {method_name}\n',
        'Arguments:  positional - {args}, named - {kwargs}\n',
        'Method result: {}\n',
    ))

    def __init__(self, log_format=default_log_format):
        self.log = []
        self.log_format = log_format

    def __str__(self):
        log_string = ''
        for method_invoke in self.log:
            log_string += self.log_format.format(**method_invoke)
        return log_string

    def __getattribute__(self, attribute_name):
        attribute = super(Logger, self).__getattribute__(attribute_name)
        if callable(attribute) and attribute_name != 'log_method':
            return self.log_method(attribute)
        else:
            return attribute

    def log_method(self, method):

        @wraps(method)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = method(*args, **kwargs)
            except Exception as ex:
                result = ex
                raise
            finally:
                self.log.append({
                    'method_name': method.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'result': result
                })

        return wrapper
