import os
import random

from django.conf import settings
from django.core.management.base import BaseCommand

from pymongo import MongoClient

from common.utils import utcnow


class Command(BaseCommand):
    help = 'Generates test data for brainblog.'

    AUTHORS = {1: 'michau'}

    MIN_TITLE = 5
    MAX_TITLE = 60

    MIN_CONTENT = 10
    MAX_CONTENT = 1000

    MIN_TAG = 1
    MAX_TAG = 10
    MAX_TAG_SUM = 100

    _number = 100
    _cleanup = True
    _text = ''
    _tag_list = []

    _path_to_files = os.path.join(settings.STATICFILES_DIRS[0], 'generator')
    _dict_path = os.path.join(_path_to_files, 'dict.txt')
    _tag_dict_path = os.path.join(_path_to_files, 'tag_dict.txt')

    def handle(self, *args, **options):
        if 'number' in options.keys():
            self._number = options.pop('number')
        if 'cleanup' in options.keys():
            self._cleanup = options.pop('cleanup')

        thoughts = []
        user_tags = {}
        self.stdout.write("Generating %d entries.\n" % self._number)
        for i in range(self._number):
            thought = {
                'author_id': long(random.choice(self.AUTHORS.keys())),
                'title': self._get_random_text(random.randint(self.MIN_TITLE, self.MAX_TITLE)),
                'content': self._get_random_text(random.randint(self.MIN_CONTENT, self.MAX_CONTENT)),
                'last_update': utcnow(),
                'tags': self._get_random_tags(random.randint(self.MIN_TAG, self.MAX_TAG)),
            }
            thought.update({'author': self.AUTHORS[thought['author_id']]})
            if thought['author_id'] not in user_tags:
                user_tags[thought['author_id']] = []
                index = []
            for tag in thought['tags']:
                if tag not in index:
                    user_tags[thought['author_id']].append({tag: 1})
                    index.append(tag)
                else:
                    i = index.index(tag)
                    user_tags[thought['author_id']][i][tag] += 1
            thoughts.append(thought)

        user_tags_ext = []
        for item in user_tags.iteritems():
            user_tag = {
                '_id': item[0],
                'tags': sorted(item[1], key=lambda t: t.values(), reverse=True)
            }
            user_tags_ext.append(user_tag)

        client = MongoClient()
        db = client[settings.DBNAME]
        if self._cleanup:
            self.stdout.write("Performing cleanup.\n")
            db.text_thought.remove()
            db.user_tags.remove()
        self.stdout.write("Saving %d thoughts and %s tag entries to db.\n" % (len(thoughts), len(user_tags_ext)))
        db.text_thought.insert(thoughts)
        db.user_tags.insert(user_tags_ext)
        client.close()

    def _get_random_text(self, length=500):
        if len(self._text) == 0:
            with open(self._dict_path) as data:
                self._text = data.read()
        if length >= len(self._text):
            return self._text
        s_index = random.randint(0, len(self._text) - length - 1)
        e_index = s_index + length
        return self._text[s_index:e_index]

    def _get_random_tags(self, length=4):
        if len(self._tag_list) == 0:
            with open(self._tag_dict_path) as data:
                self._tag_list = data.readlines()
        if length >= len(self._tag_list):
            return self._tag_list
        result = []
        sum_len = 0
        for i in range(length):
            tag = random.choice(self._tag_list)
            sum_len += len(tag)
            result.append(tag.strip())
            if sum_len >= self.MAX_TAG_SUM:
                break
        return result