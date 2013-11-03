import datetime

from django.contrib.sessions.models import Session
from django.core.cache import cache

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
    tag_dict = UserTags.objects.get(author = username).tags
    tag_size_dict = calculate_sizes(tag_dict, 1, min_size=0.5, max_size=1.5)
    cache.set('tag_size_dict', tag_size_dict)