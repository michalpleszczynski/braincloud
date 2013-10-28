from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login, logout as auth_logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm

from mongoengine import connect, connection, register_connection, ConnectionError

from tagcloud import services

from settings import DBNAME
from .models import *
from .forms import *
from .signals import *
from .daos import *


def home(request):
    return render_to_response('home.html',
                              context_instance = RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('list_thoughts'))
    else:
        form = UserRegistrationForm()
    return render_to_response('registration/register.html', {'registration_form':form},
                              context_instance = RequestContext(request))
        
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    
    if request.method == 'POST':
        redirect_to = auth_login(request)
        if request.user.is_authenticated and request.user.is_active:
            dbname = DBNAME + '_' + request.user.username
            alias = request.user.username  
            connect(dbname, alias)
        return redirect_to
    else:
        return auth_login(request)

@login_required
def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    
    alias = request.user.username
    try:
        connection.get_connection(alias).disconnect()
    except ConnectionError:
        pass
    return auth_logout(request)

@login_required
def list_thoughts(request):
    thoughts = ThoughtDao.get_all(db_name = request.user.username)
    return render_to_response('thoughts.html', {'thoughts' : thoughts},
                                  context_instance=RequestContext(request))

@login_required
def add(request):
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            new_thought = form.get_thought()
            add_tags_signal.send(sender = request.user.username, tags = new_thought.tags)
            ThoughtDao.save(new_thought, db_name = request.user.username)
            return HttpResponseRedirect(reverse('list_thoughts'))
    else:
        form = ThoughtForm()
    return render_to_response('add.html', {'thought_form': form},
                              context_instance=RequestContext(request))

@login_required
def edit(request, id):
    thought = ThoughtDao.get_by_id(id, request.user.username)
    
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            # update field values and save to mongo
            new_thought = form.get_thought()
            new_thought.id = thought.id
            update_tags_signal.send(sender = request.user.username, old_tags = thought.tags.copy(), new_tags = new_thought.tags.copy())
            ThoughtDao.save(new_thought, request.user.username)
            return HttpResponseRedirect(reverse('list_thoughts'))
    else:
        form = ThoughtForm(initial = {'title':thought.title, 'content':thought.content, 'tags':thought.get_tags_as_string()})
    return render_to_response('edit.html', {'thought_form': form},
                              context_instance=RequestContext(request))
                              
@login_required
def delete(request, id):
    thought = ThoughtDao.get_by_id(id, request.user.username)
    
    if request.method == 'POST':
        remove_tags_signal.send(sender = request.user.username, tags = thought.tags)
        ThoughtDao.remove(thought, request.user.username)
        params = {'thoughts' : ThoughtDao.get_all(request.user.username)}
        template = 'thoughts.html' 
    elif request.method == 'GET':
        params = {}
        template = 'delete.html' 
 
    return render_to_response(template, params, context_instance=RequestContext(request))