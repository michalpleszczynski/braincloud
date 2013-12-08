import datetime
import logging

from django.contrib.sessions.models import Session

from celery import task

from .index import create_thought, update_thought, delete_thought, CREATE, UPDATE, DELETE


logger = logging.getLogger(__name__)


@task(ignore_result = True)
def clear_expired_sessions():
    moment = datetime.datetime.now()
    Session.objects.filter(expire_date__lte = moment).delete()


@task(ignore_result = True)
def index_operation(thought, op_type):
    if op_type == CREATE:
        create_thought(thought)
    elif op_type == UPDATE:
        update_thought(thought)
    elif op_type == DELETE:
        delete_thought(thought)
    else:
        logger.warn('Unsupported index operation.')