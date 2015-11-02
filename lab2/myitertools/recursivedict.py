from collections import defaultdict


class DefaultDict(object):

    def __init__(self, size=100, iterable=[]):
        self._hashtable = list([] for xrange(size))

    def __getitem__(self, key):
        if key not in self:
            self[key] = DefaultDict()
        return super(self.__class__, self).__getitem__(key)

    def add_item(self, key, value):
        if not hasattr(key, '__hash__'):
            raise TypeError('Key value must be of hashable type')
        else:
            pass
