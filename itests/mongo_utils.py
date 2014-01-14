# coding: utf-8
import time
from subprocess import Popen

from django.conf import settings
from django.test.runner import DiscoverRunner

from mongoengine import connect
from mongoengine.connection import disconnect

from brainblog.index import delete_index


class MongoTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        # open elasticsearch
        es = Popen(['%s' % settings.ES_SCRIPT, '-f', '-Des.config=%s' % settings.TEST_ES_CONFIG])
        print 'Running elasticsearch...'
        time.sleep(10)
        # set up sqlite
        old_config = super(MongoTestRunner, self).setup_databases(**kwargs)
        # set up mongo
        db_name = settings.TEST_MONGODB
        disconnect()
        connect(db_name)
        print 'Creating test database: ' + db_name
        delete_index('_all')
        print 'Deleting all indexes.'
        return {'sqlite': old_config, 'mongo': db_name, 'es': es}

    def teardown_databases(self, old_config, **kwargs):
        db_name = old_config['mongo']
        old_sqlite_config = old_config['sqlite']
        es = old_config['es']
        super(MongoTestRunner, self).teardown_databases(old_sqlite_config, **kwargs)
        from pymongo import Connection
        conn = Connection()
        conn.drop_database(db_name)
        print 'Dropping test database: ' + db_name
        delete_index('_all')
        print 'Deleting all indexes.'
        es.terminate()
        message = 'Waiting for elasticsearch to terminate...'
        while not es.poll():
            time.sleep(1)
            print '\r%s' % message,
            message += '.'
        print 'Done.'