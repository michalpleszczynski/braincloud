import datetime
import operator

from django.contrib.sessions.models import Session
from django.core.cache import cache

from celery import task

from braincloud.settings import CLOUD_MAX_SIZE, CLOUD_MIN_SIZE, CLOUD_ITEMS
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
    tag_dict = UserTags.objects.get_or_create(author = username)[0].tags
    tag_dict = sorted(tag_dict.iteritems(), key=operator.itemgetter(1))
    tag_dict.reverse()
    tag_dict = dict(tag_dict[:CLOUD_ITEMS])
    tag_size_dict = calculate_sizes(tag_dict, 1, min_size=CLOUD_MIN_SIZE, max_size=CLOUD_MAX_SIZE)
    cache.set('tag_size_dict', tag_size_dict)
    return tag_size_dict