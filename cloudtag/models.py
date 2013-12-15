# coding: utf-8
from mongoengine import Document, LongField, ListField, DictField


class MySortedListField(ListField):

    _ordering = None
    _order_reverse = False

    def __init__(self, field, **kwargs):
        if 'ordering' in kwargs.keys():
            self._ordering = kwargs.pop('ordering')
        if 'reverse' in kwargs.keys():
            self._order_reverse = kwargs.pop('reverse')
        super(MySortedListField, self).__init__(field, **kwargs)

    def to_mongo(self, value):
        value = super(MySortedListField, self).to_mongo(value)
        if self._ordering is not None:
            return sorted(value, key=self._ordering,
                          reverse=self._order_reverse)
        return sorted(value, reverse=self._order_reverse)


class UserTags(Document):
    author_id = LongField(primary_key=True, unique=True)
    tags = MySortedListField(DictField(), ordering=lambda d: d.values(), reverse=True)

    def __unicode__(self):
        return "%s" % self.author

from .receivers import add_tags_receiver, update_tags_receiver, remove_tags_receiver