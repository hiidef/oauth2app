#-*- coding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
from oauth2app.models import AccessRange


@login_required
def missing_redirect_uri(request):
    return HttpResponse("Missing Redirect URI")


@login_required
def authorize_first_name(request):
    scope = AccessRange.objects.get(key="first_name")
    authorizer = Authorizer(request, scope=scope)
    try:
        authorizer.validate()
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically 
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    return authorizer.grant_redirect()

@login_required
def authorize_first_and_last_name(request):
    scope = AccessRange.objects.filter(key__in=["first_name", "last_name"])
    authorizer = Authorizer(request, scope=scope)
    try:
        authorizer.validate()
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically 
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    return authorizer.grant_redirect()

@login_required
def authorize_last_name(request):
    scope = AccessRange.objects.get(key="last_name")
    authorizer = Authorizer(request, scope=scope)
    try:
        authorizer.validate()
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically 
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    return authorizer.grant_redirect()


@login_required
def authorize_no_scope(request):
    authorizer = Authorizer(request)
    try:
        authorizer.validate()
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically 
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    return authorizer.grant_redirect()
