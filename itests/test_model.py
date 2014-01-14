# coding: utf-8
from datetime import timedelta
import time

from django.contrib.auth.models import User
from django.test import TransactionTestCase

from common.utils import timestamp, utcnow
from brainblog.models import TextThought
from brainblog.index import search_by_phrase


class TextThoughtModelTestCase(TransactionTestCase):

    def setUp(self):
        self.user = User()
        self.user.username = 'test_user'
        self.user.set_password('password')
        self.user.save()

    def _post_teardown(self):
        super(TextThoughtModelTestCase, self)._post_teardown()
        TextThought.objects.all().delete()

    def test_to_dict(self):
        self.assertEqual(TextThought.objects.count(), 0)
        thought = TextThought()
        thought.author_id = self.user.id
        thought.author = self.user.username
        thought.content = 'test content'
        thought.title = 'test title'
        thought.tags = {'tag1', 'tag2', 'tag3'}
        thought.save()
        d = thought.to_dict()
        self.assertEqual(len(d), 4)
        self.assertEqual(set(d['tags']), {'tag1', 'tag2', 'tag3'})
        self.assertEqual(d['content'], 'test content')
        self.assertEqual(d['title'], 'test title')
        now = timestamp(utcnow())
        just_now = now - 5
        self.assertTrue(now >= d['pub_date'] >= just_now)

    def test_add_thought(self):
        self.assertEqual(TextThought.objects.count(), 0)
        thought = TextThought()
        thought.author_id = self.user.id
        thought.author = self.user.username
        thought.content = 'test content'
        thought.title = 'test title'
        thought.tags = {'tag1', 'tag2', 'tag3'}
        thought.save()
        self.assertEqual(TextThought.objects.count(), 1)
        time.sleep(1)
        # test if thought was indexed
        thought_ids = search_by_phrase(self.user.id, 'test content')
        self.assertEqual(len(thought_ids), 1)
        thought = TextThought.objects.get(id=thought_ids[0])
        self.assertEqual(thought.author_id, self.user.id)
        self.assertEqual(thought.author, self.user.username)
        self.assertEqual(thought.content, 'test content')
        self.assertEqual(thought.title, 'test title')
        self.assertEqual(thought.tags, {'tag1', 'tag2', 'tag3'})
        now = utcnow()
        just_now = now - timedelta(seconds=5)
        self.assertTrue(now > thought.id.generation_time > just_now)