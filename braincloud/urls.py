from django.conf.urls.defaults import patterns, include, url

from brainblog.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', list_thoughts, name="home"),
    url(r'^add/$', add, name="add_thought"),
    url(r'^edit/(?P<id>\w+)$', edit, name="edit_thought"),
    url(r'^delete/(?P<id>\w+)$', delete, name="delete_thought"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
