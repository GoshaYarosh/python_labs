class Filtered(object):
    '''Filtered class

    Filter some sequence by some predicate.

    Usage:
        Filtered(self, some_sequence, some_predicate) -> filtered sequence
    '''

    def __init__(self, iterable, filter_func):
        self._iterable = iterable
        self._filter_func = filter_func

    def __iter__(self):
        for elem in self._iterable:
            if self._filter_func(elem):
                yield elem

    def __str__(self):
        return ' '.join(str(elem) for elem in self)


def main():
    import argparse
    import random
    import re

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--random_input', action='store_true')
    args = parser.parse_args()

    sequence = []
    if args.random_input:
        sequence = [random.randint(-10, 10) for i in range(30)]
        print ' '.join(str(elem) for elem in sequence)
    else:
        sequence = [int(number) for number in re.split(r'\s+', raw_input())]

    print 'Elems greater than zero: ', Filtered(sequence, lambda elem: elem > 0)
    print 'Even elems:', Filtered(sequence, lambda elem: elem % 2)


if __name__ == '__main__':  # pragma: no cover
    main()
