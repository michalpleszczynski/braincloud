from django.forms import ModelForm, Textarea, TextInput

from mongoengine import *

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
    tags = ListField(StringField(max_length = 30))
    
class Tag(Document):
    name = StringField(primary_key = True, max_length = 30, unique = True)
    counter = IntField()