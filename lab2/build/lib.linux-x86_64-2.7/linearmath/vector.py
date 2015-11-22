from random import random


class Vector(list):
    '''Vector class

    Represents multidimensional linear vector.

    Methods:
        __add__ - return a sum of current and other vectors
        __sub__ - return a substraction of current and other vectors
        __mul__ - if param is a vector returns dot product of current and
                  other vector, else returns vector gain
        zeros - returns a vector with all zeroes coords
        random - returns a vector with all random coords
    '''

    def __add__(self, other):
        lengths_are_equal = len(self) == len(other)
        if not lengths_are_equal:
            raise ValueError('Vectors are not the same length')
        return Vector(map(lambda x, y: x + y, self, other))

    def __sub__(self, other):
        lengths_are_eaual = len(self) == len(other)
        if not lengths_are_eaual:
            raise ValueError('Vectors are not the same length')
        return Vector(map(lambda x, y: x - y, self, other))

    def __mul__(self, other):
        if type(other) is Vector:
            lengths_are_equal = len(self) == len(other)
            if not lengths_are_equal:
                raise ValueError('Vectors are not the same length')
            return sum(map(lambda x, y: x * y, self, other))
        else:
            return Vector(map(lambda x: x * other, self))

    def __rmul__(self, other):
        return self * other

    @staticmethod
    def zeros(vector_length):
        return Vector([0 for i in xrange(vector_length)])

    @staticmethod
    def random(vector_length):
        return Vector([random() for i in xrange(vector_length)])
