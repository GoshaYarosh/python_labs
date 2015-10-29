from collections import defaultdict

class DefaultDict(dict):

    def __getitem__(self, key):
        if not key in self:
            self[key] = DefaultDict()
        return super(self.__class__, self).__getitem__(key)


dd = DefaultDict()
dd['a']['b'] = 1
print dd['a']['b']
