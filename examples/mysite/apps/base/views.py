#-*- coding: utf-8 -*-


from django.shortcuts import render_to_response
from django.template import RequestContext
from oauth2app.models import Client, AccessToken


def homepage(request):
    template = {}
    if request.user.is_authenticated():
        clients = Client.objects.filter(user=request.user)
        access_tokens = AccessToken.objects.filter(user=request.user)
        access_tokens = access_tokens.select_related()
        template["access_tokens"] = access_tokens
        template["clients"] = clients
    return render_to_response(
        'base/homepage.html', 
        template, 
        RequestContext(request))