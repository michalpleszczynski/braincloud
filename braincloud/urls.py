from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from tastypie.api import Api

from brainblog.views import *
from brainblog.api import UserResource

admin.autodiscover()

# rest api
rest_api = Api(api_name = 'rest')
rest_api.register(UserResource())
#rest_api.register(ThoughtResource())

urlpatterns = patterns(
    '',
    # thoughts
    url(r'^thoughts/$', list_thoughts, name="list_thoughts"),
    url(r'^thoughts/(?P<tag>.+)/$', list_thoughts, name="thoughts_by_tag"),
    url(r'^view_thought/(?P<id>\w+)$', view_thought, name="view_thought"),
    url(r'^add/$', add, name="add_thought"),
    url(r'^edit/(?P<id>\w+)$', edit, name="edit_thought"),
    url(r'^delete/(?P<id>\w+)$', delete, name="delete_thought"),

    # cloud
    url(r'^$', cloud, name="cloud"),

    # users
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name="logout"),
    url(r'^accounts/register/$', register, name="register"),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # search
    url(r'^search_results/$', search_thoughts),

    # rest api
    url(r'^api/', include(rest_api.urls)),
)
