class RecursiveDict(dict):
    '''RecursiveDict class

    RecursiveDict can stored values by multiply keys.

    Usage:
        rdict = RecursiveDict()
        rdict['a']['b']['c'] = 1
        print rdict['a']['b']['c']
    '''

    def __init__(self, some_dict):
        self.update(some_dict)

    def __getitem__(self, key):
        if key not in self:
            self[key] = RecursiveDict()
        return super(RecursiveDict, self).__getitem__(key)
