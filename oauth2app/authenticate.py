#-*- coding: utf-8 -*-
from urlparse import parse_qsl
from .exceptions import OAuth2Exception
from .models import AccessToken, AccessRange


class AuthenticationException(OAuth2Exception):
    error = "invalid_request"


class InvalidRequest(AuthenticationException):
    error = 'invalid_request'


class InvalidClient(AuthenticationException):
    error = 'invalid_client'


class InvalidScope(OAuth2Exception):
   pass
    

class Authenticator(object):
    
    valid = False
    access_token = None
    auth_type = None
    auth_value = None
    
    def __init__(self, request):
        self.request = request
        self.bearer_token = request.REQUEST.get('bearer_token')
        if "HTTP_AUTHORIZATION" not in self.request.META:
            auth = self.request.META["HTTP_AUTHORIZATION"].split()
            self.auth_type = auth[0].lower()
            self.auth_value = auth[1:].join(" ").strip()
            
    def validate(self):
        # Check for Bearer or Mac authorization
        if self.auth_type:
            if self.auth_type == "bearer":
                self._validate_bearer(self.auth_value)
            elif self.auth_type == "mac":
                self._validate_mac(self.auth_value)
            self.valid = True
            return
        # Check for posted/paramaterized bearer token.
        if bearer_token is not None:
            self._validate_bearer(bearer_token)
            self.valid = True
            return
        raise InvalidRequest("""Request authentication failed, no
            authentication credentials provided.""")    
    
    def _validate_bearer(self, key):
        try: 
            self.access_token = AccessToken.objects.get(key=key)
        except AccessToken.DoesNotExist:
            raise InvalidRequest("Token doesn't exist")
    
    def _validate_mac(self, auth):
        auth = parse_qsl(auth.replace(",","&").replace('"', ''))
        auth = dict([(x[0].strip(), x[1].strip()) for x in auth])
        raise NotImplementedError()
        
    def _get_user(self):
        if not self.valid:
            self.validate()
        return self.access_token.user
        
    user = property(_get_user)
    
    def _get_scope(self):
        """Client scope."""
        if not self.valid:
            self.validate()
        scopes = set(self.access_token.scope.split())
        if len(scopes) == 0:
            raise InvalidScope("Access token has no scope.")
        access_ranges = []
        for scope in scopes:
            try: 
                AccessRange.objects.get(key=scope)
            except AccessRange.DoesNotExist:
                raise InvalidScope("Scope %s does not exist." % scope)
        # Must be a better way to veryify existence then pass back a queryset.
        return AccessRange.objects.filter(key__in=scopes) 
    
    scope = property(_get_scope)

    def _get_client(self):
        if not self.valid:
            self.validate()
        return self.access_token.client
    
    client = property(_get_client)
