import json
import logging
from abc import abstractmethod

from mongoengine import Document, ListField, StringField, DateTimeField, LongField
from mongoengine import signals

from common.utils import timestamp, utcnow
from cloudtag.tasks import recalculate_cloud
from brainindex.index import DELETE, UPDATE
from .tasks import index_operation

logger = logging.getLogger(__name__)


# add Set to mongoengine, move it somewhere else later
class SetField(ListField):
    """ Extends ListField, so that's how it's represented in Mongo. """
    def __set__(self, instance, value):
        return super(SetField, self).__set__(instance, set(value) if value else set([]))

    def to_mongo(self, value):
        return super(SetField, self).to_mongo(list(value))

    def to_python(self, value):
        return set(super(SetField, self).to_python(value))

    def validate(self, value):
        if not isinstance(value, set):
            self.error('Only sets may be used.')


class BaseThought(Document):
    author = StringField()
    author_id = LongField()
    title = StringField(max_length = 60, required = True)
    last_update = DateTimeField(required = True)
    tags = SetField(StringField(max_length = 30))
    meta = {'abstract': True}

    def get_tags_as_string(self):
        return ', '.join(self.tags)

    def __unicode__(self):
        return "%s by %s" % (self.title, self.author)

    @abstractmethod
    def to_dict(self):
        return {
            'title': self.title,
            'pub_date': timestamp(self.id.generation_time),
            'tags': list(self.tags),
        }


class TextThought(BaseThought):
    content = StringField(max_length = 1000, required = True)

    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, **kwargs):
        self.last_update = utcnow()
        super(TextThought, self).save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs, **kwargs)

    def to_dict(self):
        s = super(TextThought, self).to_dict()
        s.update({'content': self.content})
        return s

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        logger.debug("Post save: %s" % document.id)
        # add new thought to index, or update existing
        index_operation.delay(document, UPDATE)
        # recalculate cloudtag
        recalculate_cloud.delay(document.author_id)

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        logger.debug("Post delete: %s" % document.id)
        index_operation.delay(document, DELETE)
        recalculate_cloud.delay(document.author_id)


signals.post_save.connect(TextThought.post_save, sender=TextThought)
signals.post_delete.connect(TextThought.post_delete, sender=TextThought)


class TextThoughtEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, TextThought):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)