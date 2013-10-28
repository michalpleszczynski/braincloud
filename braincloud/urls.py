from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from brainblog.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name="home"),
    url(r'^thoughts/$', list_thoughts, name="list_thoughts"),
    url(r'^add/$', add, name="add_thought"),
    url(r'^edit/(?P<id>\w+)$', edit, name="edit_thought"),
    url(r'^delete/(?P<id>\w+)$', delete, name="delete_thought"),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, {'next_page':'/'}, name="logout"),
    url(r'^accounts/register/$', register, name="register"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
