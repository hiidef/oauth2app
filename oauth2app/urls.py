# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from oauth2app import views
from oauth2app.token import handler

auth_view = views.AuthorizeView.as_view()

urlpatterns = patterns('',
    url(r'^missing_redirect_uri/$',
        views.MissingRedirectUriView.as_view(),
        name='oauth2app_missing_redirect_uri'),

    url(r'authorized/$',
        login_required(auth_view),
        name='oauth2app_authorize'),

    url(r'^token/$',
        handler,
        name='oauth2app_handler'),
)

