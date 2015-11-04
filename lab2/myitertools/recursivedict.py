class DefaultDict(dict):

    def __getitem__(self, key):
        if key not in self:
            self[key] = DefaultDict()
        return super(self.__class__, self).__getitem__(key)
