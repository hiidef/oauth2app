Authentication
==============

Authenticator
-------------

The Authenticator object verifies that a request has proper authentication credentials. Optionally a "scope" kwarg
of one or more AccessRange objects can be passed to verify that tokens used to access this resource are authorized
to access the specific scope.

In the event of an error the Authenticator:error_response() method will wrap an error response with
the appropriate OAuth2 headers. ::

    from oauth2app.authenticate import Authenticator, AuthenticationException
    from oauth2app.models import AccessRange
    from django.http import HttpResponse

    def test(request):
        scope = AccessRange.objects.get(key="test_scope")
        authenticator = Authenticator(scope=scope)
        try:
            # Validate the request.
            authenticator.validate(request)
        except AuthenticationException:
            # Return an error response.
            return authenticator.error_response(content="You didn't authenticate.")
        username = authenticator.user.username
        return HttpResponse(content="Hi %s, You authenticated!" % username)

JSONAuthenticator
-----------------

The JSONAuthenticator adds convenience methods and supports an optional callback request parameter
for use with JSONP requests. 

In the event of an error the JSONAuthenticator:error_response() method will return a 
JSON formatted error HttpResponse.

JSONAuthenticator:response() will serialize an object and return a formatted HttpResponse. ::

    from oauth2app.authenticate import JSONAuthenticator, AuthenticationException

    def test(request):
        authenticator = JSONAuthenticator()
        try:
            # Validate the request.
            authenticator.validate(request)
        except AuthenticationException:
            # Return a JSON encoded error response.
            return authenticator.error_response()
        username = authenticator.user.userame
        # Return a JSON encoded response.
        return authenticator.response({"username":username})

Module Reference 
----------------

.. automodule:: oauth2app.authenticate
   :members:
   :undoc-members:
   
To Do
-----

.. todo::
   MAC Authentication
   