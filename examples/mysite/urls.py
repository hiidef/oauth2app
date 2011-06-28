from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    (r'^', include('mysite.apps.base.urls')),
    (r'^account/', include('mysite.apps.account.urls')),
    (r'^client/', include('mysite.apps.client.urls')),
    (r'^oauth2/', include('mysite.apps.oauth2.urls')),
    (r'^api/', include('mysite.apps.api.urls')),
)
