import json

from django.utils import timezone

from mongoengine import Document, ListField, StringField, DateTimeField

from common.utils import timestamp


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


class ThoughtEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Thought):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)