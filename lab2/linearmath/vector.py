from random import random

class Vector(object):

    def __init__(self, coords=list()):
        self.coords = coords

    def __len__(self):
        return len(self.coords)

    def __iter__(self):
        return self.coords.__iter__()

    def __getitem__(self, index):
        return self.coords[index]

    def __setitem__(self, index, coord):
        self.coords[index] = coord

    def __str__(self):
        return '(' + ', '.join((str(coord) for coord in self)) + ')'

    def __eq__(self, other):
        lengths_are_equal = len(self) == len(other)
        elements_are_equal = all(map(lambda x, y: x == y, self, other))
        return lengths_are_equal and elements_are_equal

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
