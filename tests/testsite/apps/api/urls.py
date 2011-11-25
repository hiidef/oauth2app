#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('testsite.apps.api.views',
    (r'^automatic_error_str/?$',        'automatic_error_str'),
    (r'^automatic_error_json/?$',       'automatic_error_json'),
    (r'^first_name_str/?$',             'first_name_str'),
    (r'^first_and_last_name_str/?$',    'first_and_last_name_str'),
    (r'^last_name_str/?$',              'last_name_str'),
    (r'^email_str/?$',                  'email_str'),
    (r'^email_json/?$',                 'email_json'))
    