# coding: utf-8
from django.test import Client
from django.test import TransactionTestCase
from django.contrib.auth.models import User

from cloudtag.models import UserTags


class ThoughtViewTest(TransactionTestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='michau', email='test@test.test')
        self.user.set_password('test')
        self.user.save()
        # create tag holder for the new user
        self.user_tags = UserTags()
        self.user_tags.author_id = self.user.id
        self.user_tags.save()
        ret = self.client.login(username=self.user.username, password='test')
        self.assertTrue(ret)

    def test_empty_thought_view(self):
        resp = self.client.get('/thoughts/')
        self.assertEqual(resp.status_code, 200)
