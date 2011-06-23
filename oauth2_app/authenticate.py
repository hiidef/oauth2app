#-*- coding: utf-8 -*-


from .exceptions import OAuth2Exception


class AuthenticationException(OAuth2Exception):
    error = "invalid_request"


class Authenticator(object):
    
    valid = False
    
    def __init__(self, request):
        pass
    
    def validate(self):
        self.valid = True
    
    def get_user(self):
        if not self.valid:
            self.validate()
        raise NotImplementedError()
        
    user = property(get_user)
    
    def get_scope(self):
        if not self.valid:
            self.validate()
        raise NotImplementedError()
    
    scope = property(get_scope)

    def get_client(self):
        if not self.valid:
            self.validate()
        raise NotImplementedError()
    
    client = property(get_client)
