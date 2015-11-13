class LinearFunction(object):
    '''LinearFunction class

    Represents a linear fucntion of the form: f(x) = Ax + B,
    where A and B some coeffs

    Methods:
        __init__ - initialize coeffs of linear function
        __call__ - if param is other linear function returns a
                   composition of current and other function, else
                   returns a substitution of value into function
        __add__ - returns a sum of current and other linear functions
        __sub__ - returns a substraction of current and other functions
        __mul__ - returns a multiply of current function on some number
    '''

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, param):
        if isinstance(param, LinearFunction):
            other_function = param
            composition = LinearFunction(
                self.a * other_function.a,
                self.a * other_function.b + self.b
            )
            return composition
        elif isinstance(param, (int, long, float)):
            point = param
            return self.a * point + self.b
        else:
            raise TypeError('Wrong param type: {0}'.format(type(param)))

    def __str__(self):
        result_string = 'f(x) = '
        if self.a == 0 and self.b == 0:
            return result_string + '0'
        else:
            if self.a == 0:
                result_string += ''
            elif self.a == 1:
                result_string += 'x'
            elif self.a == -1:
                result_string += '-x'
            else:
                result_string += '{0}x'.format(self.a)
            if self.b == 0:
                result_string += ''
            elif self.b > 0 and self.a == 0:
                result_string += '{0}'.format(self.b)
            elif self.b > 0 and self.a != 0:
                result_string += ' + {0}'.format(self.b)
            elif self.b < 0:
                result_string += ' - {0}'.format(-self.b)
            return result_string

    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)

    def __add__(self, other):
        return LinearFunction(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return LinearFunction(self.a - other.a, self.b - other.b)

    def __mul__(self, number):
        return LinearFunction(self.a * number, self.b * number)
