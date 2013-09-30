from django.db.models.signals import pre_save
from django.dispatch import receiver

from mongoengine import *

from tagcloud import services

from .signals import *

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

class User(Document):
    username = StringField(max_length = 30, required = True, unique = True)
    # for now
    password = StringField(max_length = 30, required = True)
    email = EmailField(max_length = 40, required = True, unique = True)

class Thought(Document):
    author = ReferenceField(User)
    title = StringField(max_length = 120, required = True)
    content = StringField(max_length = 1000, required = True)
    last_update = DateTimeField(required = True)
    tags = SetField(StringField(max_length = 30))
    
    def get_tags_as_string(self):
        return ', '.join(self.tags)
    
@receiver(update_tags_signal)
def update_tags(sender, **kwargs):
    services.update_tags(kwargs['old_tags'], kwargs['new_tags'])

@receiver(add_tags_signal)    
def add_tags(sender, **kwargs):
    services.add_tags(kwargs['tags'])
    
@receiver(remove_tags_signal)
def remove_tags(sender, **kwargs):
    services.remove_tags(kwargs['tags'])