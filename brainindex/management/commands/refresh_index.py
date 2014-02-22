# coding: utf-8
from django.core.management.base import BaseCommand

from brainblog.models import TextThought
from ...index import update_thought, delete_index


class Command(BaseCommand):
    help = 'Refresh elasticsearch index. Usage: python manage.py refresh_index <index_name>'

    _index_name = '_all'

    def handle(self, *args, **options):
        if len(args) == 1:
            self._index_name = args[0]
        else:
            ans = raw_input("All indexes will be cleared. Are you sure you want to continue? (y/n)")
            if ans.lower() != 'y':
                return

        print 'Clearing index: %s' % self._index_name
        delete_index(self._index_name)
        if self._index_name == '_all':
            for thought in TextThought.objects.all():
                update_thought(thought)
        else:
            for thought in TextThought.objects.filter(author=self._index_name):
                update_thought(thought)