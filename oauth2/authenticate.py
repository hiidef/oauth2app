#-*- coding: utf-8 -*-


from .exceptions import OAuth2Exception


class AuthenticationException(OAuth2Exception):
    error = "invalid_request"

class NotImplemented(OAuth2Exception):
    pass


class Authenticator(object):
    
    valid = False
    
    def __init__(self, request):
        pass
    
    def validate(self):
        self.valid = True
    
    def get_user(self):
        if not self.valid:
            self.validate()
        raise NotImplemented()
        
    user = property(get_user)
    
    def get_scope(self):
        if not self.valid:
            self.validate()
        raise NotImplemented()
    
    scope = property(get_scope)

    def get_client(self):
        if not self.valid:
            self.validate()
        raise NotImplemented()
    
    client = property(get_client)
