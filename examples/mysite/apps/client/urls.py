#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',)

urlpatterns = patterns('mysite.apps.client.views',
    (r'^(?P<client_id>\w+)/?$', 'client'),
)  # Create your views here.
