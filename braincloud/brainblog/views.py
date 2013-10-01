from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from tagcloud import services

from .models import *
from .forms import ThoughtForm
from .signals import *


def list_thoughts(request):
    thoughts = Thought.objects.all()
    return render_to_response('thoughts.html', {'thoughts' : thoughts},
                              context_instance=RequestContext(request))

@login_required
def add(request):
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            new_thought = form.get_thought()
            add_tags_signal.send(sender = Thought, tags = new_thought.tags)
            new_thought.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ThoughtForm()
    return render_to_response('add.html', {'thought_form': form},
                              context_instance=RequestContext(request))

def edit(request, id):
    thought = Thought.objects.get(id=id)
    
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            # update field values and save to mongo
            new_thought = form.get_thought()
            new_thought.id = thought.id
            update_tags_signal.send(sender = Thought, old_tags = thought.tags, new_tags = new_thought.tags.copy())
            new_thought.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ThoughtForm(initial = {'title':thought.title, 'content':thought.content, 'tags':thought.get_tags_as_string()})
    return render_to_response('edit.html', {'thought_form': form},
                              context_instance=RequestContext(request))
                              

def delete(request, id):
    thought = Thought.objects.get(id=id)
    
    if request.method == 'POST':
        remove_tags_signal.send(sender = Thought, tags = thought.tags)
        thought.delete()
        params = {'thoughts':Thought.objects.all()}
        template = 'thoughts.html' 
    elif request.method == 'GET':
        params = {}
        template = 'delete.html' 
 
    return render_to_response(template, params, context_instance=RequestContext(request))