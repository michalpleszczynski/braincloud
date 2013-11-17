from braincloud.common.utils import is_collection

from .models import UserTags


def add_tags(username, tags):
    user_tags, created = UserTags.objects.get_or_create(author = username)
    # if single string than make it a list to have the same logic for both
    if not is_collection(tags):
        tags = [tags]
    # get only keys in the list, lookup in this list and then access the full list by index
    tag_list = [i.keys()[0] for i in user_tags.tags]
    for tag in tags:
        try:
            index = tag_list.index(tag)
            user_tags.tags[index][tag] += 1
        except ValueError:
            user_tags.tags.append({tag: 1})
    user_tags.save()


def remove_tags(username, tags):
    user_tags = UserTags.objects.get(author = username)
    if not is_collection(tags):
        tags = [tags]
    # see add_tags
    tag_list = [i.keys()[0] for i in user_tags.tags]
    for tag in tags:
        index = tag_list.index(tag)
        user_tags.tags[index][tag] -= 1
        if user_tags.tags[index] == 0:
            del user_tags.tags[index]
    user_tags.save()


def update_tags(username, old_tags, new_tags):
    if old_tags == new_tags:
        return
    # extract common tags
    common = new_tags.intersection(old_tags)
    # remove them from both sets
    only_new_tags = new_tags - common
    old_tags -= common

    # add new and remove old
    add_tags(username, only_new_tags)
    remove_tags(username, old_tags)
