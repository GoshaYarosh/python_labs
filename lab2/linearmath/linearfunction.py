class LinearFunction(object):

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
        else:
            point = param
            return self.a * point + self.b

    def __str__(self):
        if self.a == 0 and self.b == 0:
            return result_string + '0'
        else:
            result_string = 'f(x) = '
            if self.a == 0:
                result_string += ''
            elif self.a == 1:
                result_string += 'x'
            elif self.a == -1:
                result_string += '-x'
            else:
                result_string += '{0}x'.format(a)
            if self.b == 0:
                result_string += ''
            elif self.b > 0:
                result_string += '+ {0}'.format(self.b)
            elif self.b < 0:
                result_string += '- {0}'.format(self.b)
            return result_string

    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)

    def __add__(self, other):
        return LinearFunction(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return LinearFunction(self.a - other.a, self.b - other.b)

    def __mul__(self, number):
        return LinearFunction(self.a * number, self.b * number)
