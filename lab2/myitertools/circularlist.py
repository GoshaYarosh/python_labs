class CircularList(list):

    def __iter__(self):
        elems = super(CircularList, self)
        if elems.__len__() > 0:
            while True:
                for elem in elems.__iter__():
                    yield elem

    def __getitem__(self, index):
        if isinstance(index, slice):
            items = [
                self[index]
                for index in xrange(index.start, index.stop, index.step)
            ]
            return items
        else:
            items = super(CircularList, self)
            return items.__getitem__(index % items.__len__())

    def __getslice__(self, start, stop):
        start = start - len(self) if start < 0 else start
        stop = stop - len(self) if stop < 0 else stop
        return self[start:stop:1]

    def iteritems(self, items_count):
        for index, item in enumerate(self):
            yield item
            if index > items_count:
                break

    def itercycles(self, cycles_count):
        items_count = cycles_count * len(self)
        for index, item in enumerate(self):
            if index < items_count:
                yield item
            else:
                break

    def filter(self, predicate):
        for item in self.itercycles(1):
            if predicate(item):
                self.remove(item)
