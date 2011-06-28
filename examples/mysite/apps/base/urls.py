#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mysite.apps.base.views',
    (r'^/?$',                      'homepage'),
)