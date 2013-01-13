from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    (r'^oauth2/', include('testsite.apps.oauth2.urls')),
    (r'^api/', include('testsite.apps.api.urls')),
)
