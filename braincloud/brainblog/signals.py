import django.dispatch

update_tags_signal = django.dispatch.Signal(providing_args=["new_tags","old_tags"])

add_tags_signal = django.dispatch.Signal(providing_args=["tags"])

remove_tags_signal = django.dispatch.Signal(providing_args=["tags"])