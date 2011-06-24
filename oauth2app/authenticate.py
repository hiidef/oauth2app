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
    
    def __init__(self, request):
        self.request = request
    
    def validate(self):
        if "HTTP_AUTHORIZATION" not in self.request.META:
            raise InvalidRequest("""Request authentication failed, no
                authentication credentials provided.""")
        auth = self.request.META["HTTP_AUTHORIZATION"].split()
        auth_type = auth[0].lower()
        if auth_type in ["bearer"]:
            self._validate_bearer(auth[1])
        elif auth_type in ["mac"]:
            self._validate_mac(auth[1:].join(" "))        
        self.valid = True
    
    def _validate_bearer(self, key):
        try: 
            self.access_token = AccessToken.objects.get(key=key)
        except AccessToken.DoesNotExist:
            raise InvalidRequest("Token doesn't exist")
    
    def _validate_mac(self, auth):
        auth = parse_qsl(auth.replace(",","&").replace('"', ''))
        auth = dict([(x[0].strip(), x[1].strip()) for x in auth])
        raise NotImplementedError()
        
    def get_user(self):
        if not self.valid:
            self.validate()
        return self.access_token.user
        
    user = property(get_user)
    
    def get_scope(self):
        scopes = set(self.access_token.scope.split())
        if len(scopes) == 0:
            raise InvalidScope("Access token has no scope.")
        access_ranges = []
        for scope in scopes:
            try: 
                AccessRange.objects.get(key=scope)
            except AccessRange.DoesNotExist:
                raise InvalidScope("Access range %s does not exist." % scope)
        if not self.valid:
            self.validate()
        # Must be a better way to veryify existence then pass back a queryset.
        return AccessRange.objects.filter(key__in=scopes) 
    
    scope = property(get_scope)

    def get_client(self):
        if not self.valid:
            self.validate()
        return self.access_token.client
    
    client = property(get_client)
