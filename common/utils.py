import datetime
import time

from pytz import utc

from collections import Iterable


def is_collection(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, basestring)


def timestamp(val=None):
    """
    Returns datetime object as timestamp.
    """
    if not val:
        return int(time.time())
    else:
        return int(time.mktime(val.timetuple()))


def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=utc)