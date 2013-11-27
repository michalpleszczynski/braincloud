# coding: utf-8
from django.core.cache import cache
from django.conf import settings

from celery import task

from .models import UserTags
from .services import calculate_sizes

@task(ignore_result = True)
def recalculate_cloud(username):
    user = UserTags.objects.get(author = username)
    if user is None:
        return {}
    tag_list = user.tags[:settings.CLOUD_ITEMS]
    tag_dict = {k: v for d in tag_list for k, v in d.items()}
    tag_size_dict = calculate_sizes(tag_dict, 1, min_size=settings.CLOUD_MIN_SIZE, max_size=settings.CLOUD_MAX_SIZE)
    cache.set(username + 'tag_size_dict', tag_size_dict)
    return tag_size_dict