#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from oauth2app.token import TokenGenerator
from oauth2app.consts import MAC

urlpatterns = patterns('',
        (r'^missing_redirect_uri/?$',           'testsite.apps.oauth2.views.missing_redirect_uri'),
        (r'^authorize_not_refreshable/?$',      'testsite.apps.oauth2.views.authorize_not_refreshable'),     
        (r'^authorize_mac/?$',                  'testsite.apps.oauth2.views.authorize_mac'),        
        (r'^authorize_first_name/?$',           'testsite.apps.oauth2.views.authorize_first_name'),
        (r'^authorize_first_name/?$',           'testsite.apps.oauth2.views.authorize_last_name'),
        (r'^authorize_first_and_last_name/?$',  'testsite.apps.oauth2.views.authorize_first_and_last_name'),
        (r'^authorize_no_scope/?$',             'testsite.apps.oauth2.views.authorize_no_scope'),
        (r'^authorize_code/?$',                 'testsite.apps.oauth2.views.authorize_code'),
        (r'^authorize_token/?$',                'testsite.apps.oauth2.views.authorize_token'),
        (r'^authorize_token_mac/?$',            'testsite.apps.oauth2.views.authorize_token_mac'),
        (r'^authorize_code_and_token/?$',       'testsite.apps.oauth2.views.authorize_code_and_token'),
        (r'^token/?$',                          'oauth2app.token.handler'),
        (r'^token_mac/?$',                      TokenGenerator(authentication_method=MAC))
)

