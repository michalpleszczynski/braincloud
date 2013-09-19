from django.forms import ModelForm, Textarea, TextInput

from mongoengine import *

class Thought(Document):
    title = StringField(max_length = 120, required = True)
    content = StringField(max_length = 1000, required = True)
    last_update = DateTimeField(required = True)
    tags = ListField(StringField(max_length = 30))
    
class Tag(Document):
    name = StringField(primary_key = True, max_length = 30, unique = True)
    counter = IntField()