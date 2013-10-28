import datetime

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from mongoengine import connection, ConnectionError
from celery import task

@task(ignore_result=True)
def clear_expired_sessions():
    #moment = datetime.datetime.now()
    #sessions = Session.objects.filter(expire_date__lte=moment)
    #for s in sessions:
    #    # TODO: change to user id
    #    username = User.objects.filter(id=s.get_decoded()['_auth_user_id']).username
    #    try:
    #        connection.get_connection(username).disconnect()
    #    except ConnectionError:
    #        pass
    Session.objects.filter(expire_date__lte=moment).delete()