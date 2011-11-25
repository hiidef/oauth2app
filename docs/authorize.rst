Authorization
=============

Authorizer
----------

The authorizer grants access tokens and authentication codes via query string parameters and URI fragments
sent to redirect URIs. Optionally a "scope" kwarg of one or more AccessRange objects can be passed to verify 
that granted tokens can only be used to access specific scopes.

In the event of an error the Authorizer:error_response() method will return a redirect response to the 
client's redirect_uri with information on the error passed as query string parameters.

If a request is authorized, Authorizer:grant_response() will serialize an object into a JSON response will 
return a redirect response to the client's redirect_uri with information on the authorization code passed as query string parameters (response_type CODE) or access token passed as URI fragments. ::

    from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
    from oauth2app.models import AccessRange
        
    @login_required
    def authorize(request):
        scope = AccessRange.objects.get(key="last_login")
        authorizer = Authorizer(scope=scope)
        try:
            # Validate the request.
            authorizer.validate(request)
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

Module Reference 
----------------

.. automodule:: oauth2app.authorize
   :members:
   :undoc-members:
