from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .utils import calculate_sizes


def home(request):
    return render_to_response('home.html',
                              context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # create tag holder for the new user
            user_tags = UserTags
            user_tags.author = new_user.username
            user_tags.save()
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
        thoughts = Thought.objects.filter(author = request.user.username, tags__contains = tag)
    return render_to_response('thoughts.html', {'thoughts': thoughts},
                              context_instance = RequestContext(request))


@login_required
def add(request):
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            new_thought = form.get_thought()
            new_thought.author = request.user.username
            add_tags_signal.send(sender=request.user.username, tags=new_thought.tags)
            new_thought.save()
            return HttpResponseRedirect(reverse('list_thoughts'))
    else:
        form = ThoughtForm()
    return render_to_response('add.html', {'thought_form': form},
                              context_instance=RequestContext(request))


@login_required
def edit(request, id):
    thought = Thought.objects.get(id=id)

    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            # update field values and save to mongo
            new_thought = form.get_thought()
            new_thought.id = thought.id
            update_tags_signal.send(sender=request.user.username, old_tags=thought.tags,
                                    new_tags=new_thought.tags)
            new_thought.save()
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
        params = {'thoughts': Thought.objects.filter(author=request.user.username)}
        template = 'thoughts.html'
    elif request.method == 'GET':
        params = {}
        template = 'delete.html'

    return render_to_response(template, params, context_instance=RequestContext(request))


@login_required
def cloud(request):
    tag_dict = UserTags.objects.get(author = request.user.username).tags
    tag_size_dict = calculate_sizes(tag_dict, min_size=0.5, max_size=1.5)
    return render_to_response('cloud.html', {'tags': tag_size_dict},
                              context_instance= RequestContext(request))
