# coding: utf-8
from braincloud.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.db'),
    },
}

TEST_MONGODB = 'braincloud_mongo_test'

# tests run a lot faster by using this algorithm
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
TEST_RUNNER = 'itests.mongo_utils.MongoTestRunner'

# run celery tasks right away
CELERY_ALWAYS_EAGER = True

# use test index
ELASTICSEARCH_URL = '127.0.0.1:9991'