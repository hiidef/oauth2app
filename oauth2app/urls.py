from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('',
    url(r'^authorize/$', views.AuthorizeView.as_view(), name='authorize'),
    url(r'^token/$', 'oauth2app.token.handler', name='token'),
)