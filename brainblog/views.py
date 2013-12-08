import logging

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.utils import timezone

from cloudtag.models import UserTags
from cloudtag.tasks import recalculate_cloud
from cloudtag.signals import add_tags_signal, remove_tags_signal, update_tags_signal
from .forms import ThoughtForm, UserRegistrationForm
from .models import Thought
from .tasks import index_operation
from .index import CREATE, UPDATE, DELETE


logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # create tag holder for the new user
            new_user_tags = UserTags()
            new_user_tags.author = request.user.username
            new_user_tags.save()

            return HttpResponseRedirect(reverse('list_thoughts'))
    else:
        form = UserRegistrationForm()
    return render_to_response('registration/register.html', {'registration_form': form},
                              context_instance=RequestContext(request))


@login_required
def list_thoughts(request, tag = None):
    if not tag:
        thoughts = Thought.objects.filter(author = request.user.username)
    else:
        # workaround for tags with whitespace in them
        tag = tag.replace('/', ' ')
        thoughts = Thought.objects.filter(author = request.user.username, tags__contains = tag)
    return render_to_response('thoughts.html', {'thoughts': thoughts},
                              context_instance = RequestContext(request))


@login_required
def view_thought(request, id):
    thought = Thought.objects.get(id=id)

    return render_to_response('view_thought.html', {'thought': thought},
                              context_instance = RequestContext(request))


@login_required
def add(request):
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            new_thought = form.get_thought()
            new_thought.author = request.user.username
            new_thought.pub_date = timezone.now()
            add_tags_signal.send(sender=request.user.username, tags=new_thought.tags)
            new_thought.save()
            index_operation.delay(new_thought, CREATE)
            recalculate_cloud.delay(request.user.username)
            return HttpResponseRedirect(reverse('list_thoughts'))
    else:
        form = ThoughtForm()
    return render_to_response('add.html', {'thought_form': form},
                              context_instance = RequestContext(request))


@login_required
def edit(request, id):
    thought = Thought.objects.get(id=id)

    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            # update field values and save to mongo
            new_thought = form.get_thought()
            new_thought.id = thought.id
            new_thought.pub_date = thought.pub_date
            update_tags_signal.send(sender=request.user.username, old_tags=thought.tags,
                                    new_tags=new_thought.tags)
            new_thought.save()
            index_operation.delay(new_thought, UPDATE)
            recalculate_cloud.delay(request.user.username)
            return HttpResponseRedirect(reverse('list_thoughts'))
    else:
        form = ThoughtForm(initial={'title': thought.title, 'content': thought.content,
                                    'tags': thought.get_tags_as_string()})
    return render_to_response('edit.html', {'thought_form': form},
                              context_instance=RequestContext(request))


@login_required
def delete(request, id):
    thought = Thought.objects.get(id=id)

    if request.method == 'POST':
        remove_tags_signal.send(sender=request.user.username, tags=thought.tags)
        thought.delete()
        index_operation.delay(thought, DELETE)
        recalculate_cloud.delay(request.user.username)
        params = {'thoughts': Thought.objects.filter(author=request.user.username)}
        template = 'thoughts.html'
    elif request.method == 'GET':
        params = {}
        template = 'delete.html'

    return render_to_response(template, params, context_instance=RequestContext(request))


@login_required
def cloud(request):
    username = request.user.username
    tag_size_dict = cache.get(username + 'tag_size_dict')
    if not tag_size_dict:
        logger.info('tag_size_dict not in cache')
        tag_size_dict = recalculate_cloud(username)
        cache.set(username + 'tag_size_dict', tag_size_dict)
    return render_to_response('cloud.html', {'tags': tag_size_dict},
                              context_instance= RequestContext(request))
