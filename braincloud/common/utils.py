from collections import Iterable

def is_collection(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, basestring)