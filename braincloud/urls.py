from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from brainblog.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name="home"),

    # thoughts
    url(r'^thoughts/$', list_thoughts, name="list_thoughts"),
    url(r'^thoughts/(?P<tag>\w+)$', list_thoughts, name="thoughts_by_tag"),
    url(r'^add/$', add, name="add_thought"),
    url(r'^edit/(?P<id>\w+)$', edit, name="edit_thought"),
    url(r'^delete/(?P<id>\w+)$', delete, name="delete_thought"),

    # cloud
    url(r'cloud/$', cloud, name="cloud"),

    # users
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name="logout"),
    url(r'^accounts/register/$', register, name="register"),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
