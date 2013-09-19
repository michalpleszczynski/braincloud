import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from .models import *
from .forms import ThoughtForm

def add(request):
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_thought = Thought(title = cd['title'], content = cd['content'])
            new_thought.tags = add_tags([item.strip() for item in cd['tags'].split(",")])
            new_thought.last_update = datetime.datetime.now()
            new_thought.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ThoughtForm()
    # Get all posts from DB
    thoughts = Thought.objects.all()
    return render_to_response('index.html', {'thoughts': thoughts, 'thought_form': form},
                              context_instance=RequestContext(request))
    
    def add_tags(tags):
        for tag in tags:
            Tag.objects(name=tag).update_one(inc__counter=1, upsert = True)
        return tags

def update(request):
    id = eval("request." + request.method + "['id']")
    thought = Thought.objects.filter(id=id)[0]
    
    if request.method == 'POST':
        # update field values and save to mongo
        thought.title = request.POST['title']
        thought.last_update = datetime.datetime.now() 
        thought.content = request.POST['content']
        thought.save()
        template = 'index.html'
        params = {'Thoughts': Thought.objects.all()} 

    elif request.method == 'GET':
        template = 'update.html'
        params = {'thought':thought}
   
    return render_to_response(template, params, context_instance=RequestContext(request))
                              

def delete(request):
    id = eval("request." + request.method + "['id']")

    if request.method == 'POST':
        thought = Thought.objects.filter(id=id)[0]
        thought.delete() 
        template = 'index.html'
        params = {'Thoughts': Thought.objects.all()} 
    elif request.method == 'GET':
        template = 'delete.html'
        params = { 'id': id } 

    return render_to_response(template, params, context_instance=RequestContext(request))