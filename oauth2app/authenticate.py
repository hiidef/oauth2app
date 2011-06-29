#-*- coding: utf-8 -*-


from django.http import HttpResponse, HttpResponseBadRequest
from urlparse import parse_qsl
from .exceptions import OAuth2Exception
from .models import AccessToken, AccessRange


class AuthenticationException(OAuth2Exception):
    """Authentication exception base class."""
    pass


class InvalidRequest(AuthenticationException):
    """The request is missing a required parameter, includes an
    unsupported parameter or parameter value, repeats the same
    parameter, uses more than one method for including an access
    token, or is otherwise malformed."""
    error = 'invalid_request'


class InvalidToken(AuthenticationException):
    """The access token provided is expired, revoked, malformed, or
    invalid for other reasons."""
    error = 'invalid_token'


class InsufficientScope(AuthenticationException):
    """The request requires higher privileges than provided by the
    access token."""
    error = 'insufficient_scope'

    
class Authenticator(object):
    """Django HttpRequest authenticator. Checks a request for valid
    credentials and scope.
    
    **Args:**
    
    * *request:* Django HttpRequest object.
    
    **Kwargs:**
    
    * *scopes:* A iterable of oauth2app.models.AccessRange objects.
    """
    
    valid = False
    access_token = None
    auth_type = None
    auth_value = None
    error = None
    
    def __init__(self, request, scope=None):
        if scope is None:
            self.authorized_scope = None
        elif isinstance(scope, AccessRange):
            self.authorized_scope = set([scope.key])
        else:
            self.authorized_scope = set([x.key for x in scope])
        self.request = request
        self.bearer_token = request.REQUEST.get('bearer_token')
        if "HTTP_AUTHORIZATION" in self.request.META:
            auth = self.request.META["HTTP_AUTHORIZATION"].split()
            self.auth_type = auth[0].lower()
            self.auth_value = " ".join(auth[1:]).strip()

    
    def validate(self):
        """Validate the request. Raises an AuthenticationException if the 
        request fails authentication.
        
        *Returns None*"""
        try:
            self._validate()
        except AuthenticationException, e:
            self.error = e
            raise e
        self.valid = True
        
    def _validate(self):
        # Check for Bearer or Mac authorization
        if self.auth_type:
            if self.auth_type == "bearer":
                self._validate_bearer(self.auth_value)
            elif self.auth_type == "mac":
                self._validate_mac(self.auth_value)
            self.valid = True
        # Check for posted/paramaterized bearer token.
        elif self.bearer_token is not None:
            self._validate_bearer(self.bearer_token)
            self.valid = True
            return
        else:
            raise InvalidRequest("""Request authentication failed, no
                authentication credentials provided.""")    
        if self.authorized_scope is not None:
            token_scope = set([x.key for x in self.access_token.scope.all()])
            new_scope = self.authorized_scope - token_scope
            if len(new_scope) > 0:
                raise InsufficientScope("""Access token has insufficient 
                    scope: %s""" % list(new_scope))
            
    def _validate_bearer(self, token):
        """Validate Bearer token."""
        try: 
            self.access_token = AccessToken.objects.get(token=token)
        except AccessToken.DoesNotExist:
            raise InvalidToken("Token doesn't exist")
    
    def _validate_mac(self, auth):
        """Validate MAC authentication. Not implemented."""
        auth = parse_qsl(auth.replace(",","&").replace('"', ''))
        auth = dict([(x[0].strip(), x[1].strip()) for x in auth])
        raise NotImplementedError()
        
    def _get_user(self):
        """The user associated with the valid access token. 
        
        *django.auth.User object*"""
        if not self.valid:
            self.validate()
        return self.access_token.user
        
    user = property(_get_user)
    
    def _get_scope(self):
        """The client scope associated with the valid access token.
        
        *QuerySet of AccessRange objects.*"""
        if not self.valid:
            self.validate()
        return self.access_token.scope.all()
    
    scope = property(_get_scope)

    def _get_client(self):
        """The client associated with the valid access token. 
       
        *oauth2app.models.Client object*"""
        if not self.valid:
            self.validate()
        return self.access_token.client
    
    client = property(_get_client)
    
    def error_response(self, error=None):
        """In the event of an error, return a Django HttpResponseBadRequest
        with the appropriate JSON encoded error parameters.

        *Returns HttpResponseBadRequest*"""
        if error is not None:
            e = error
        elif self.error is not None:
            e = self.error
        else:
            e = InvalidRequest("Access Denied.")
        error = getattr(e, "error", "invalid_request")
        error_description = e.message

        return HttpResponseBadRequest(    
            content=json_data, 
            content_type='application/json')