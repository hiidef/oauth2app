
* See http://hiidef.github.com/oauth2app for documentation. 
* See https://github.com/hiidef/oauth2app for source code.
* Based on http://code.google.com/p/django-oauth2
* Support for OAuth 2.0 draft 16, http://tools.ietf.org/html/draft-ietf-oauth-v2-16

Installation
------------

If easy_install is available, you can use: ::

    easy_install https://github.com/hiidef/oauth2app/tarball/master

Introduction
------------

The oauth2app module helps Django site operators provide an OAuth 2.0 interface. The module
is registered as an application.

In settings.py, add 'oauth2app' to INSTALLED_APPS. ::


    INSTALLED_APPS = (
        ...,
        'oauth2app' 
    )

Sync the DB models. ::

    python manage.py syncdb

In urls.py, add /oauth2/authorize and /oauth2/token views to a new or existing app. ::

    urlpatterns += patterns('',
        (r'^oauth2/missing_redirect_uri/?$',   'mysite.oauth2.views.missing_redirect_uri'),
        (r'^oauth2/authorize/?$',                'mysite.oauth2.views.authorize'),
        (r'^oauth2/token/?$',                    'oauth2app.token.handler'),
    )
    
Create client models. ::

    from oauth2app.models import Client

    Client.objects.create(
        name="My Sample OAuth 2.0 Client",
        user=user)

Create authorize and missing_redirect_uri handlers. ::

    from django.shortcuts import render_to_response
    from django.http import HttpResponseRedirect
    from django.template import RequestContext
    from django.contrib.auth.decorators import login_required
    from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
    from django import forms

    class AuthorizeForm(forms.Form):
        pass

    @login_required
    def missing_redirect_uri(request):
        return render_to_response(
            'oauth2/missing_redirect_uri.html', 
            {}, 
            RequestContext(request))

    @login_required
    def authorize(request):
        authorizer = Authorizer(request)
        try:
            # Validate the request.
            authorizer.validate()
        except MissingRedirectURI, e:
            # No redirect_uri was specified.
            return HttpResponseRedirect("/oauth2/missing_redirect_uri")
        except AuthorizationException, e:
            # The request is malformed or invalid. Redirect to redirect_uri with error params.
            return authorizer.error_redirect()
        if request.method == 'GET':
            template = {}
            # Use any form, make sure it has CSRF protections.
            template["form"] = AuthorizeForm()
            # Appends the original OAuth2 parameters.
            template["form_action"] = '/oauth2/authorize?%s' % authorizer.query_string
            return render_to_response(
                'oauth2/authorize.html', 
                template, 
                RequestContext(request))
        elif request.method == 'POST':
            form = AuthorizeForm(request.POST)
            if form.is_valid():
                if request.POST.get("connect") == "Yes":
                    # User agrees. Redirect to redirect_uri with success params.
                    return authorizer.grant_redirect()
                else:
                    # User refuses. Redirect to redirect_uri with error params.
                    return authorizer.error_redirect()
        return HttpResponseRedirect("/")

Authenticate requests. ::

    from oauth2app.authenticate import Authenticator, AuthenticationException

    def email(request):
        authenticator = Authenticator(request)
        try:
            # Validate the request.
            authenticator.validate()
        except AuthenticationException:
            # Return a JSON encoded error response.
            return authenticator.error_response()
        # Return a JSON encoded success response.
        return authenticator.grant_response({"email":request.user.email})    

Examples
--------

An `example Django project <https://github.com/hiidef/oauth2app/tree/develop/examples/mysite>`_ demonstrating client and server functionality is available in the repository.

https://github.com/hiidef/oauth2app/tree/develop/examples/mysite
