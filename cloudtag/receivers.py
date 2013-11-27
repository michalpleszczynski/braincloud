from django.dispatch import receiver

from .signals import *
from .services import *


@receiver(update_tags_signal)
def update_tags_receiver(sender, **kwargs):
    update_tags(sender, kwargs['old_tags'], kwargs['new_tags'])


@receiver(add_tags_signal)    
def add_tags_receiver(sender, **kwargs):
    add_tags(sender, kwargs['tags'])


@receiver(remove_tags_signal)
def remove_tags_receiver(sender, **kwargs):
    remove_tags(sender, kwargs['tags'])