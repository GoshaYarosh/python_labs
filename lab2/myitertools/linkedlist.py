class LinkedListNode(object):
    """Node of linked list:

    Stores some value and references on next and previous nodes of list.

    Attributes:
        node_value - the value stored in current node
        next_node - the next node of current (default value is None)
        prev_node - the previous node of current (default value is None)
    """

    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value
        self.next_node = next_node
        self.prev_node = prev_node


class LinkedList(object):
    """Linked list:

    Values stored in nodes of list. Every node has
    references on next and previous nodes of list. You can create list from
    some iterable, add and remove values from list in random place.
    Also supports indexation by integer index, iteration on the values,
    filtering by some predicate.

    Public methods:
        add_first(value) - add value on first position
        add_last(value) - add value on last position
        insert_at(value, index) - insert value on the index'th position
        remove_first(value) - return and remove the first value
        remove_last(value) - return and remove the last value
        remove_at(value) - return and remove the value from index'th position
        filter(predicate) - remove all values that match the predicate
        find_value(predicate) - return first value that match the predicate
    """

    def __init__(self, iterable=[]):
        self._first_node = None
        self._last_node = None
        self._length = 0
        for value in iterable:
            self.add_last(value)

    def __iter__(self):
        current_node = self._first_node
        while current_node is not None:
            yield current_node.value
            current_node = current_node.next_node

    def __len__(self):
        return self._length

    def __str__(self):
        return '|' + " ".join(str(value) for value in self) + '|'

    def __getitem__(self, index):
        if isinstance(index, slice):
            return (
                self._get_node(ind)
                for ind in xrange(index.start, index.stop, index.step)
            )
        else:
            return self._get_node(index).value

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            for ind in xrange(index.start, index.stop, index.step):
                self._get_node(ind).value = value
        else:
            self._get_node(index).value = value

    def __delitem__(self, index):
        if isinstance(index, slice):
            for ind in xrange(index.start, index.stop, index.step):
                self.remove_at(ind)
        else:
            self.remove_at(index)

    def _get_node(self, index):
        # check the index bounds
        if index >= self._length:
            raise IndexError('Index is out of list size')
        # iterating in list to index'th position
        current_node = self._first_node
        while index > 0:
            index -= 1
            current_node = current_node.next_node
        return current_node

    def add_first(self, value):
        self._length += 1
        new_node = LinkedListNode(value, None, self._first_node)
        if self._first_node is not None:
            # list is not empty set previous to first node
            self._first_node.prev_node = new_node
            self._first_node = new_node
        else:
            # list is empty. value is the first and the last
            self._first_node = new_node
            self._last_node = new_node

    def add_last(self, value):
        self._length += 1
        new_node = LinkedListNode(value, self._last_node, None)
        if self._last_node is not None:
            # list is not empty set previous to first node
            self._last_node.next_node = new_node
            self._last_node = new_node
        else:
            # list is empty. value is the first and the last
            self._first_node = new_node
            self._last_node = new_node

    def remove_first(self):
        if self._first_node is not None:
            self._length -= 1
            removable_node = self._first_node
            if removable_node.next_node is not None:
                # list contains more than one value
                removable_node.next_node.prev_node = None
                self._first_node = removable_node.next_node
            else:
                # list contains one value
                self._first_node = None
                self._last_node = None
            return removable_node.value
        else:
            # list is empty
            raise IndexError('List is empty')

    def remove_last(self):
        if self._last_node is not None:
            self._length -= 1
            removable_node = self._last_node
            if removable_node.prev_node is not None:
                # list contains more than one value
                removable_node.prev_node.next_node = None
                self._last_node = removable_node.prev_node
            else:
                # list contains one value
                self._first_node = None
                self._last_node = None
            return removable_node.value
        else:
            # list is empty
            raise IndexError('List is empty')

    def insert_at(self, value, index):
        current_node = self._get_node(index)
        if current_node is self._first_node:
            self.add_first(value)
        else:
            self._length += 1
            new_node = LinkedListNode(
                value,
                current_node.prev_node,
                current_node
            )
            current_node.prev_node.next_node = new_node
            current_node.prev_node = new_node

    def remove_at(self, index):
        current_node = self._get_node(index)
        if current_node is self._first_node:
            return self.remove_first()
        elif current_node is self._last_node:
            return self.remove_last()
        else:
            self._length -= 1
            current_node.prev_node.next_node = current_node.next_node
            current_node.next_node.prev_node = current_node.prev_node
            return current_node.value

    def filter(self, predicate):
        index = 0
        for value in self:
            if not predicate(value):
                del self[index]
            else:
                index += 1

    def find_value(self, predicate):
        for index, value in enumerate(self):
            if predicate(value):
                return index
