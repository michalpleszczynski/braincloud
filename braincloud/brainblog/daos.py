from mongoengine.context_managers import switch_db

from common.utils import is_collection

from .models import *


class ThoughtDao(object):

    @staticmethod
    def get_all(db_name):
        with switch_db(Thought, db_name) as data:
            return data.objects.all()
        
    @staticmethod
    def get_by_id(id, db_name):
        with switch_db(Thought, db_name) as data:
            return data.objects.get(id=id)
        
    @staticmethod
    def save(thought, db_name):
        with switch_db(Thought, db_name) as data:
            thought.save()
            
    @staticmethod
    def remove(thought, db_name):
        with switch_db(Thought, db_name) as data:
            thought.delete()
