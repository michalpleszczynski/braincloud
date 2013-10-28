from collections import Iterable

from mongoengine.context_managers import switch_db

from common.utils import is_collection

from .models import *

class TagDao(object):
    
    @staticmethod
    def create_or_update(tags, db_name):
        with switch_db(Tag, db_name) as data:
            if is_collection(tags):
                for tag in tags:
                    data.objects(name=tag).update_one(inc__counter=1, upsert = True)
            else:
                data.objects(name=tags).update_one(inc__counter=1, upsert = True)
                
    @staticmethod
    def decrement_and_remove(tags, db_name):
        with switch_db(Tag, db_name) as data:
            if is_collection(tags):
                for tag in tags:
                    data.objects(name=tag).update_one(inc__counter=-1, upsert = False)
            else:
                data.objects(name=tags).update_one(inc__counter=-1, upsert = False)
            # remove all the unused tags
            data.objects(counter=0).delete()