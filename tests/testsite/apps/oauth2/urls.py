#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        (r'^missing_redirect_uri/?$',           'testsite.apps.oauth2.views.missing_redirect_uri'),
        (r'^authorize_first_name/?$',           'testsite.apps.oauth2.views.authorize_first_name'),
        (r'^authorize_first_name/?$',           'testsite.apps.oauth2.views.authorize_last_name'),
        (r'^authorize_first_and_last_name/?$',  'testsite.apps.oauth2.views.authorize_first_and_last_name'),
        (r'^authorize_no_scope/?$',             'testsite.apps.oauth2.views.authorize_no_scope'),
        (r'^token/?$',                          'oauth2app.token.handler'),
)