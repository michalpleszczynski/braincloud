# coding: utf-8
from django.core.cache import cache
from django.conf import settings

from celery import task
from celery.utils.log import get_task_logger

from .models import UserTags
from .services import calculate_sizes


logger = get_task_logger(__name__)


@task(ignore_result = True)
def recalculate_cloud(user_id):
    logger.debug('Recalculating cloud')
    user = UserTags.objects.get(author_id = user_id)
    if user is None:
        return {}
    tag_list = user.tags[:settings.CLOUD_ITEMS]
    tag_dict = {k: v for d in tag_list for k, v in d.items()}
    tag_size_dict = calculate_sizes(tag_dict, 1, min_size=settings.CLOUD_MIN_SIZE, max_size=settings.CLOUD_MAX_SIZE)
    cache.set(str(user_id) + 'tag_size_dict', tag_size_dict)
    return tag_size_dict