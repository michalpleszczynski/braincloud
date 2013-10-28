from .daos import *

# point of access to tags from other apps

def add_tags(db_name, tags):
    TagDao.create_or_update(tags, db_name)

def remove_tags(db_name, tags):
    TagDao.decrement_and_remove(tags, db_name)

def update_tags(db_name, old_tags, new_tags):
    if old_tags == new_tags:
        return
    # extract common tags
    common = new_tags.intersection(old_tags)
    # remove them from both sets
    new_tags -= common
    old_tags -= common

    # add new and remove old
    add_tags(db_name, new_tags)
    remove_tags(db_name, old_tags)
        