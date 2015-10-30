from functools import wraps


class Logger(object):

    format_string = 'Invoke method: {0}\nArguments: positional - {1}, named - {2}\nResult: {3}\n\n'

    def log_method(self, function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = function(*args, **kwargs)
            except Exception as ex:
                result = 'raised exception'
            finally:
                self.log += Logger.format_string.format(
                    function.__name__,
                    args,
                    kwargs,
                    result,
                )

        return wrapper

    def __init__(self):
        self.log = ''

    def __getattribute__(self, attribute_name):
        attribute = super(Logger, self).__getattribute__(attribute_name)
        if attribute_name == 'log_method':
            return attribute
        elif hasattr(attribute, '__call__'):
            return self.log_method(attribute)
        else:
            return attribute


logger = Logger()
logger.some_method = lambda x, y: x + y
logger.another_method = lambda x: x ** 2
logger.some_method(1, 2)
logger.another_method(10)
logger.some_method('a', 'b')

print logger.log
