class LinearFunction(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, point):
        return self.a * point + self.b

    def __str__(self):
        return "f(x) = {0}x + {1}".format(self.a, self.b)

    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)

    def __add__(self, other):
        return LinearFunction(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return LinearFunction(self.a - other.a, self.b - other.b)

    def __mul__(self, number):
        return LinearFunction(self.a * number, self.b * number)
