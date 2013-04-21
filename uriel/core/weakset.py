# Gregory Rosenblatt

from weakref import ref


class WeakSet(object):
    """A set which weakly references its contents."""

    def __init__(self, sequence=[]):
        self.set = set(sequence)

    def __iter__(self):
        return iter(self.set)

    def Add(self, obj):
        self.set.add(ref(obj, self.set.remove))

    def Remove(self, obj):
        self.set.remove(ref(obj))
