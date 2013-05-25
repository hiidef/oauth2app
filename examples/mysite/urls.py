
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # enable admin interface
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('mysite.apps.base.urls')),
    (r'^account/', include('mysite.apps.account.urls')),
    (r'^client/', include('mysite.apps.client.urls')),
    (r'^oauth2/', include('mysite.apps.oauth2.urls')),
    (r'^api/', include('mysite.apps.api.urls')),
)

