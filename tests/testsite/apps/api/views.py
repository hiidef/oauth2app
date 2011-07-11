#-*- coding: utf-8 -*-


from oauth2app.authenticate import Authenticator, JSONAuthenticator
from oauth2app.authenticate import AuthenticationException
from oauth2app.models import AccessRange
from django.http import HttpResponse


def first_name_str(request):
    scope = AccessRange.objects.get(key="first_name")
    authenticator = Authenticator(request, scope=scope)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.first_name)


def last_name_str(request):
    scope = AccessRange.objects.get(key="last_name")
    authenticator = Authenticator(request, scope=scope)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.last_name)

def first_and_last_name_str(request):
    scope = AccessRange.objects.filter(key__in=["first_name", "last_name"])
    authenticator = Authenticator(request, scope=scope)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.last_name)

def email_str(request):
    authenticator = Authenticator(request)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.email)


def email_json(request):
    authenticator = JSONAuthenticator(request)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response({"email":authenticator.user.email})


