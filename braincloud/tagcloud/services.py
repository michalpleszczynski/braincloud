from .models import Tag

# point of access to tags from other apps

def add_tags(tags):
    for tag in tags:
        Tag.objects(name=tag).update_one(inc__counter=1, upsert = True)
    return tags

def remove_tags(tags):
    for tag in tags:
        Tag.objects(name=tag).update_one(inc__counter=-1, upsert = False)
    # remove all the unused tags
    Tag.objects(counter=0).delete()
    return tags

def update_tags(old_tags, new_tags):
    if old_tags == new_tags:
        return
    # extract common tags
    common = new_tags.intersection(old_tags)
    # remove them from both sets
    new_tags -= common
    old_tags -= common

    # add new and remove old
    add_tags(new_tags)
    remove_tags(old_tags)
        