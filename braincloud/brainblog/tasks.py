import datetime

from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.conf import settings

from celery import task

from braincloud.brainblog.models import UserTags
from braincloud.brainblog.utils import calculate_sizes


@task(ignore_result = True)
def clear_expired_sessions():
    moment = datetime.datetime.now()
    Session.objects.filter(expire_date__lte = moment).delete()


@task(ignore_result = True)
def create_user_tags(username):
    new_user_tags = UserTags()
    new_user_tags.author = username
    new_user_tags.save()


@task(ignore_result = True)
def recalculate_cloud(username):
    user = UserTags.objects.get(author = username)
    if user is None:
        return {}
    tag_list = user.tags[:settings.CLOUD_ITEMS]
    tag_dict = {k: v for d in tag_list for k, v in d.items()}
    tag_size_dict = calculate_sizes(tag_dict, 1, min_size=settings.CLOUD_MIN_SIZE, max_size=settings.CLOUD_MAX_SIZE)
    cache.set('tag_size_dict', tag_size_dict)
    return tag_size_dict