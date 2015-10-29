from unittest import TestCase
from random import randint, shuffle, random

from classtools.cache import cached
from myitertools.myrange import myrange
from myitertools.sort import external_sort
from linearmath.vector import Vector
from linearmath.linearfunction import LinearFunction


class VectorTest(TestCase):
    vector_length = 10 * 1000
    coords = [randint(-10, 10) for i in xrange(vector_length)]
    vector = Vector(coords)

    def test_equality(self):
        self.assertEqual(self.vector, self.vector)
        self.assertEqual(self.vector, Vector(self.coords))
        self.assertNotEqual(self.vector, self.vector[::-1])

    def test_length(self):
        self.assertEqual(len(self.vector), self.vector_length)
        self.assertEqual(len(Vector()), 0)

    def test_iterator(self):
        self.assertItemsEqual(self.vector, self.coords)
        self.assertItemsEqual(Vector(), [])

    def test_operations(self):
        self.assertEqual(self.vector * 2, 2 * self.vector)
        self.assertEqual(self.vector * 0, Vector.zeros(self.vector_length))
        self.assertEqual(self.vector + self.vector, self.vector * 2)
        self.assertEqual(self.vector - self.vector, self.vector * 0)
        self.assertEqual(self.vector * self.vector, self.vector * self.vector)


class LinearFunctionTest(TestCase):

    def test_substitution(self):
        function = LinearFunction(random(), random())
        self.assertEqual(function(0), function.b)
        self.assertEqual(function(1), function.a + function.b)

    def test_addition(self):
        function = LinearFunction(random(), random())
        self.assertEqual(function + function, function * 2)
        self.assertEqual(function - function, LinearFunction(0, 0))


class CachedDecoratorTest(TestCase):

    @cached
    def cached_sum(self, numbers):
        self.number_of_calls += 1
        return sum(numbers)

    def test_cached_function(self):
        self.number_of_calls = 0
        numbers_count = 3
        numbers = [randint(-10, 10) for i in xrange(numbers_count)]
        self.cached_sum(numbers)
        self.assertEqual(self.cached_sum(numbers), sum(numbers))
        self.assertEqual(self.number_of_calls, 1)
        self.assertEqual(self.cached_sum(numbers), self.cached_sum(numbers))
        self.assertEqual(self.cached_sum(numbers), sum(numbers))
        self.assertNotEqual(self.cached_sum(numbers[:-1]),
                            self.cached_sum(numbers))
        self.assertEqual(self.number_of_calls, 2)


class MyRangeTest(TestCase):

    def test_myrange(self):
        self.assertItemsEqual(myrange(10), xrange(10))
        self.assertItemsEqual(myrange(10, 100), xrange(10, 100))
        self.assertItemsEqual(myrange(1, 10000, 2), xrange(1, 10000, 2))
        self.assertItemsEqual(myrange(10, 1, -1), xrange(10, 1, -1))
        self.assertItemsEqual(myrange(1, 10, -1), xrange(1, 10, -1))
        with self.assertRaises(ValueError):
            sum(myrange(10, 100, 0))


class ExternalSortTest(TestCase):
    nums_count = 30
    testfile_name = 'test.numbers'

    def init_testfile(self):
        numbers = (randint(-10000, 10000) for i in xrange(self.nums_count))
        lines = ['{0}\n'.format(number) for number in numbers]
        with open(self.testfile_name, 'w') as testfile:
            testfile.truncate(0)
            testfile.writelines(lines)
        return lines

    def test_external_sort(self):
        lines = self.init_testfile()
        lines = sorted(lines, key=int)
        external_sort(self.testfile_name)
        with open(self.testfile_name, 'r') as testfile:
            self.assertItemsEqual(testfile.readlines(), lines)

    def test_reverse_external_sort(self):
        lines = self.init_testfile()
        lines = sorted(lines, key=int, reverse=True)
        external_sort(self.testfile_name, reverse=True)
        with open(self.testfile_name, 'r') as testfile:
            self.assertItemsEqual(testfile.readlines(), lines)

    def test_chunk_size_exception(self):
        lines = self.init_testfile()
        with self.assertRaises(ValueError):
            external_sort(self.testfile_name, chunk_size=0)
            external_sort(self.testfile_name, chunk_size=-100)
