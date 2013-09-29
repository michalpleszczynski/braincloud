from mongoengine import *

class Tag(Document):
    name = StringField(primary_key = True, max_length = 30, unique = True)
    counter = IntField()