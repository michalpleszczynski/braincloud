import json
import logging

from django.utils import timezone

from mongoengine import Document, ListField, StringField, DateTimeField, LongField
from mongoengine import signals

from common.utils import timestamp
from cloudtag.tasks import recalculate_cloud
from .index import DELETE, UPDATE
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


class Thought(Document):
    author = StringField()
    author_id = LongField()
    title = StringField(max_length = 60, required = True)
    content = StringField(max_length = 1000, required = True)
    last_update = DateTimeField(required = True)
    pub_date = DateTimeField(required = True)
    tags = SetField(StringField(max_length = 30))

    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, **kwargs):
        self.last_update = timezone.now()
        super(Thought, self).save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs, **kwargs)

    def get_tags_as_string(self):
        return ', '.join(self.tags)

    def __unicode__(self):
        return "%s by %s" % (self.title, self.author)

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'pub_date': timestamp(self.pub_date),
            'tags': list(self.tags),
        }

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


signals.post_save.connect(Thought.post_save, sender=Thought)
signals.post_delete.connect(Thought.post_delete, sender=Thought)


class ThoughtEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Thought):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)