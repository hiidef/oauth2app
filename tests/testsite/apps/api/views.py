#-*- coding: utf-8 -*-


from oauth2app.authenticate import Authenticator, JSONAuthenticator
from oauth2app.authenticate import AuthenticationException
from oauth2app.models import AccessRange
from django.http import HttpResponse

def automatic_error_str(request):
    authenticator = Authenticator()
    return authenticator.error_response()

def automatic_error_json(request):
    authenticator = JSONAuthenticator()
    return authenticator.error_response()

def first_name_str(request):
    scope = AccessRange.objects.get(key="first_name")
    authenticator = Authenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.first_name)


def last_name_str(request):
    scope = AccessRange.objects.get(key="last_name")
    authenticator = Authenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.last_name)

def first_and_last_name_str(request):
    scope = AccessRange.objects.filter(key__in=["first_name", "last_name"])
    authenticator = Authenticator(scope=scope)
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.first_name +  " " + authenticator.user.last_name)

def email_str(request):
    authenticator = Authenticator()
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return HttpResponse(authenticator.user.email)


def email_json(request):
    authenticator = JSONAuthenticator()
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response({"email":authenticator.user.email})


