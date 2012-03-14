from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from apps.oauth2.views import CustomAuthorizeView

urlpatterns = patterns('',
    (r'^', include('mysite.apps.base.urls')),
    (r'^account/', include('mysite.apps.account.urls')),
    (r'^client/', include('mysite.apps.client.urls')),
    #(r'^oauth2/', include('mysite.apps.oauth2.urls')),
    (r'^api/', include('mysite.apps.api.urls')),

    # Override authorize url to use my custom view
    url(r'oauth2/authorize/',
        CustomAuthorizeView.as_view(),
        name='oauth2app_authorize'),

    # Hook oauth2app urls
    url(r'oauth2/', include('oauth2app.urls')),
)

