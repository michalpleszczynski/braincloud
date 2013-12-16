# coding: utf-8
import datetime
import time

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.utils import timezone

from brainblog.models import Thought
from brainblog.index import search_by_phrase


class AddThoughtTestCase(TransactionTestCase):

    def setUp(self):
        self.user = User()
        self.user.username = 'test_user'
        self.user.set_password('password')
        self.user.save()

    def test_add_thought(self):
        self.assertEqual(Thought.objects.count(), 0)
        thought = Thought()
        thought.author_id = self.user.id
        thought.author = self.user.username
        thought.content = 'test content'
        thought.title = 'test title'
        thought.tags = {'tag1', 'tag2', 'tag3'}
        thought.pub_date = timezone.now()
        thought.save()
        self.assertEqual(Thought.objects.count(), 1)
        time.sleep(1)
        # test if thought was indexed
        thought_ids = search_by_phrase(self.user.id, 'test content')
        self.assertEqual(len(thought_ids), 1)
        thought = Thought.objects.get(id=thought_ids[0])
        self.assertEqual(thought.author_id, self.user.id)
        self.assertEqual(thought.author, self.user.username)
        self.assertEqual(thought.content, 'test content')
        self.assertEqual(thought.title, 'test title')
        self.assertEqual(thought.tags, {'tag1', 'tag2', 'tag3'})
        self.assertTrue(timezone.now() > thought.pub_date > timezone.now() - datetime.timedelta(seconds=5))