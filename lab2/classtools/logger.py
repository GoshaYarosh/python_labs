from functools import wraps


class Logger(object):

    default_log_format = ''.join((
        'Method: {}\n',
        'Arguments:  positional - {}, named - {}\n',
        'Method result: {}\n',
    ))

    def __init__(self, log_format=default_log_format):
        self.log = []
        self.log_format = log_format

    def __str__(self):
        log_string = ''
        for method_invoke in self.log:
            log_string += self.log_format.format(
                method_invoke['method_name'],
                method_invoke['args'],
                method_invoke['kwargs'],
                method_invoke['result'],
            )
        return log_string

    def __getattribute__(self, attribute_name):
        attribute = super(Logger, self).__getattribute__(attribute_name)
        if attribute_name == 'log_method':
            return attribute
        elif hasattr(attribute, '__call__'):
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
