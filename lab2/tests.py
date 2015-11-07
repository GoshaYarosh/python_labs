from unittest import TestCase
from random import randint, random
from classtools.cache import cached

from classtools.logger import Logger
from classtools.json import to_json, from_json
from classtools.sigleton import Singleton
from linearmath.linearfunction import LinearFunction
from linearmath.vector import Vector
from myitertools.linkedlist import LinkedList
from myitertools.myrange import myrange
from myitertools.sort import external_sort


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

    def test_string_representation(self):
        pass

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
        self.init_testfile()
        with self.assertRaises(ValueError):
            external_sort(self.testfile_name, chunk_size=0)
            external_sort(self.testfile_name, chunk_size=-100)


class LoggerTest(TestCase):

    class LoggedClass(Logger):

        def instance_method(self, a, b):
            return a + b

    def test_logger(self):
        logged_class = LoggerTest.LoggedClass()
        logged_class.instance_method(10, 20)
        with self.assertRaises(TypeError):
            logged_class.instance_method(10, '20')
            logged_class.instance_method(object(), object())
        self.assertEqual(logged_class.log[0]['result'], 30)
        self.assertEqual(logged_class.log[0]['method_name'], 'instance_method')
        self.assertNotEqual(logged_class.log[1]['result'], 30)


class LinkedListTest(TestCase):

    def test_adding_values(self):
        values = []
        linked_list = LinkedList()
        for i in xrange(100):
            value = randint(-1000, 1000)
            values.append(value)
            linked_list.add_last(value)
        self.assertItemsEqual(linked_list, values)

        for i in xrange(100):
            value = randint(-1000, 1000)
            values = [value] + values
            linked_list.add_first(value)
        self.assertItemsEqual(linked_list, values)

        for i in xrange(50):
            index = randint(0, len(linked_list) - 1)
            value = randint(-10, 10)
            values = values[:index] + [value] + values[index:]
            linked_list.insert_at(value, index)
        self.assertItemsEqual(linked_list, values)

    def test_removing_values(self):
        values = [randint(-1000, 1000) for i in xrange(400)]
        linked_list = LinkedList(values)
        for i in xrange(100):
            self.assertEqual(values.pop(), linked_list.remove_last())
        self.assertItemsEqual(values, linked_list)

        for i in xrange(100):
            self.assertEqual(values[0], linked_list.remove_first())
            values = values[1:]
        self.assertItemsEqual(values, linked_list)

        for i in xrange(100):
            index = randint(0, len(linked_list) - 1)
            self.assertEqual(values[index], linked_list.remove_at(index))
            del values[index]
        self.assertItemsEqual(values, linked_list)

    def test_indexing(self):
        values = [randint(-1000, 1000) for i in xrange(400)]
        linked_list = LinkedList(values)
        for i in range(100):
            index = randint(0, len(linked_list) - 1)
            self.assertEqual(values[index], linked_list[index])

        for i in range(100):
            index = randint(0, len(linked_list) - 1)
            value = randint(-1000, 1000)
            values[index] = value
            linked_list[index] = value
        self.assertItemsEqual(values, linked_list)

        for i in range(100):
            index = randint(0, len(linked_list) - 1)
            del values[index]
            del linked_list[index]
        self.assertItemsEqual(values, linked_list)

    def test_filtering(self):
        values = [randint(-1000, 1000) for i in xrange(1000)]
        linked_list = LinkedList(values)
        predicates = [
            lambda value: value > 0,
            lambda value: value % 2 == 0,
            lambda value: value ** 2 < 10000
        ]
        for predicate in predicates:
            values = filter(predicate, values)
            linked_list.filter(predicate)
            self.assertItemsEqual(values, linked_list)


class JsonTest(TestCase):

    def test_from_json(self):
        obj = {
            'a': 1,
            'b': '2',
            'c': [1, 2, ['1', '2', '3'], 3],
        }
        json_string = '{"a": 1, "b": "2", "c": [1, 2, ["1", "2", "3"], 3]}'
        self.assertEqual(from_json(json_string), obj)

        obj = {
            'a': [1, 2, True],
            'b': {'a': None, 'b': 1.0},
            'c': [{'a': False}, [1, 2, None], "pipka"],
            'd': {'a': 10, 'b': {'a': 20}}
        }
        json_string = """{
            "a": [1, 2, true], "c": [{"a": false}, [1, 2, null], "pipka"]
            "b": {"a": null, "b": 1.0},
            "d": {"a": 10, "b": {"a": 20}}
        }"""
        self.assertEqual(from_json(json_string), obj)

    def test_to_json(self):
        obj = {
            'a': 1,
            'b': '2',
            'c': [1, 2, ['1', '2', '3'], 3],
        }
        self.assertEqual(from_json(to_json(obj)), obj)

        obj = {
            'a': [1, 2, True],
            'b': {'a': None, 'b': 1.0},
            'd': {'a': 10, 'b': {'a': 20}},
            'c': [{'a': False}, [1, 2, None], "pipka"],
        }
        self.assertEqual(from_json(to_json(obj)), obj)


class SingletonTest(TestCase):

    @Singleton
    class SingletonedClass(object):
        def __init__(self, some_arg):
            self.arg = some_arg

    def test_singleton(self):
        first_obj = SingletonTest.SingletonedClass(10)
        second_obj = SingletonTest.SingletonedClass(20)
        self.assertTrue(first_obj is second_obj)
        self.assertEqual(first_obj.arg, second_obj.arg, 10)
        del first_obj
        first_obj = SingletonTest.SingletonedClass(30)
        self.assertTrue(first_obj is second_obj)
        self.assertEqual(first_obj.arg, second_obj.arg, 10)
