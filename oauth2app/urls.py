from django.conf.urls import url

from . import views
from .token import handler as token_handler

app_name = 'oauth2app'

urlpatterns = [
    url(r'^authorize/$', views.AuthorizeView.as_view(), name='authorize'),
    url(r'^token/$', token_handler, name='token'),
]
