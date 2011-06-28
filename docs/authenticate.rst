Authentication
==============

Authenticator
-------------

The Authenticator object verifies that a request has proper authentication credentials. Optionally a "scope" kwarg
of one or more AccessRange objects can be passed to verify that tokens used to access this resource are authorized
to access the specific scope.

In the event of an error the Authenticator:error_response() method will return a standard error response.

If a request is authenticated, Authenticator:grant_response() will serialize an object into a JSON response. ::

    from oauth2app.authenticate import Authenticator, AuthenticationException
    from oauth2app.models import AccessRange
    
    def email(request):
        scope = AccessRange.objects.get(key="last_login")
        authenticator = Authenticator(request, scope=scope)
        try:
            # Validate the request.
            authenticator.validate()
        except AuthenticationException:
            # Return a JSON encoded error response.
            return authenticator.error_response()
        # Return a JSON encoded success response.
        return authenticator.grant_response({"email":request.user.email})

Module Reference 
----------------

.. automodule:: oauth2app.authenticate
   :members:
   :undoc-members: