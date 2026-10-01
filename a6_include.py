# Minimal stand-ins for the course helper classes, matching the methods hashmap.py uses.


class DynamicArray:
    """A thin wrapper around a Python list."""

    def __init__(self):
        self._data = []

    def append(self, value):
        self._data.append(value)

    def length(self):
        return len(self._data)

    def get_at_index(self, index):
        return self._data[index]

    def __getitem__(self, index):
        return self._data[index]


class SLNode:
    """One key/value node in a bucket's chain."""

    def __init__(self, key, value, next=None):
        self.key = key
        self.value = value
        self.next = next

    def __str__(self):
        return f"({self.key}: {self.value})"


class LinkedList:
    """A singly linked list of key/value nodes (one per hash bucket)."""

    def __init__(self):
        self._head = None
        self._size = 0

    def insert(self, key, value):
        self._head = SLNode(key, value, self._head)
        self._size += 1

    def remove(self, key):
        prev, cur = None, self._head
        while cur:
            if cur.key == key:
                if prev:
                    prev.next = cur.next
                else:
                    self._head = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def length(self):
        return self._size

    def __iter__(self):
        cur = self._head
        while cur:
            yield cur
            cur = cur.next

    def __str__(self):
        return " -> ".join(str(node) for node in self)


def hash_function_1(key: str) -> int:
    """Sum of the character codes."""
    return sum(ord(c) for c in key)


def hash_function_2(key: str) -> int:
    """Character codes weighted by position, so 'ab' and 'ba' hash differently."""
    return sum((i + 1) * ord(c) for i, c in enumerate(key))