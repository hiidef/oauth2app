#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mysite.apps.account.views',
    (r'^login/?$',                  'login'),
    (r'^logout/?$',                 'logout'),
    (r'^signup/?$',                 'signup'),
    (r'^clients/?$',                'clients'),
)