#-*- coding: utf-8 -*-

from .exceptions import OAuth2Exception
from .models import Client


class AuthenticationException(OAuth2Exception):
    error = "invalid_request"


class InvalidRequest(AuthenticationException):
    error = 'invalid_request'


class InvalidClient(AuthenticationException):
    error = 'invalid_client'


class Authenticator(object):
    
    valid = False
    client = None
    
    def __init__(self, request):
        self.client_id = request.REQUEST.get('client_id')
    
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
