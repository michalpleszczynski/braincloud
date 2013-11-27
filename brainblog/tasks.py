import datetime

from django.contrib.sessions.models import Session

from celery import task


@task(ignore_result = True)
def clear_expired_sessions():
    moment = datetime.datetime.now()
    Session.objects.filter(expire_date__lte = moment).delete()