# coding: utf-8
from django.core.management.base import BaseCommand

from brainblog.models import Thought
from brainblog.index import update_thought


class Command(BaseCommand):
    help = 'Refresh elasticsearch index.'

    def handle(self, *args, **options):
        for thought in Thought.objects.all():
            update_thought(thought)