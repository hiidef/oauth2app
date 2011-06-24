#-*- coding: utf-8 -*-


from django.http import absolute_http_url_re, HttpResponseRedirect
from .exceptions import OAuth2Exception
from .models import Client, AccessRange, Code, AccessToken
from .lib.response import RESPONSE_TYPES, TOKEN, CODE, CODE_AND_TOKEN, is_valid_response_type
from .consts import ACCESS_TOKEN_EXPIRATION
from .lib.uri import add_parameters, add_fragments, normalize


class AuthorizationException(OAuth2Exception):
    error = 'invalid_request'


class MissingRedirectURI(OAuth2Exception):
    pass


class UnauthenticatedUser(OAuth2Exception):
    pass


class UnvalidatedRequest(OAuth2Exception):
    pass
    

class InvalidRequest(AuthorizationException):
    error = 'invalid_request'


class InvalidClient(AuthorizationException):
    error = 'invalid_client'


class UnauthorizedClient(AuthorizationException):
    error = 'unauthorized_client'


class RedirectURIMismatch(AuthorizationException):
    error = 'redirect_uri_mismatch'


class AccessDenied(AuthorizationException):
    error = 'access_denied'


class UnsupportedResponseType(AuthorizationException):
    error = 'unsupported_response_type'


class InvalidScope(AuthorizationException):
    error = 'invalid_scope'


def authorize(request):
    authorizer = Authorizer(request)
    try:
        authorizer.validate()
    except MissingRedirectURI, e:
        # Return a 500 or something.
        pass
    except AuthorizationException, e:
        # Invalid request.
        return authorizer.error_redirect()
    try:
        return authorizer.grant_redirect()
    except UnvalidatedRequest, e:
        pass
        # The validate() method must be run before grant().
    except UnauthenticatedUser, e:
        # request.user.is_authenticated() is false. Log the user in.
        pass

    
class Authorizer(object):
    
    client = None
    valid = False
    error = None
    
    def __init__(self, request):
        self.response_type = request.REQUEST.get('response_type')
        self.client_id = request.REQUEST.get('client_id')
        self.redirect_uri = request.REQUEST.get('redirect_uri')
        self.scope = request.REQUEST.get('scope')
        self.state = request.REQUEST.get('state')
        self.user = request.user
        self.request = request

    def validate(self):
        try:
            self._validate()
        except AuthorizationException, e:
            self.check_redirect_uri()
            self.error = e
            raise e
        self.valid = True
    
    def _validate(self):
        if self.client_id is None:
            raise InvalidRequest('No client_id')
        try: 
            self.client = Client.objects.get(key=self.client_id)
        except Client.DoesNotExist:
            raise InvalidClient("client_id %s doesn't exist" % self.client_id)
        # Redirect URI
        if self.redirect_uri is None:
            if self.client.redirect_uri is None:
                raise MissingRedirectURI("""No redirect_uri 
                    provided or registered.""")
        elif self.client.redirect_uri is not None:
            if normalize(self.redirect_uri) != normalize(self.client.redirect_uri):
                self.redirect_uri = self.client.redirect_uri
                raise RedirectURIMismatch("""Registered redirect_uri doesn't
                    match provided redirect_uri.""")
        self.redirect_uri = self.redirect_uri or self.client.redirect_uri
        # Check response type
        if self.response_type is None:
            raise InvalidRequest('response_type is a required parameter.')
        if self.response_type not in RESPONSE_TYPES:
            raise InvalidRequest("""No such response 
                type: %s""" % self.response_type)
        # Response type
        if not is_valid_response_type(
                RESPONSE_TYPES[self.response_type], 
                self.client.authorized_reponse_types):
            raise UnauthorizedClient("""Response type %s not allowed for
                client""" % self.response_type)        
        if not absolute_http_url_re.match(self.redirect_uri):
            raise InvalidRequest('Absolute URI required for redirect_uri')
        # Scope 
        if self.scope is not None:
            scopes = set(self.scope.split())
            access_ranges = AccessRange.objects.filter(key__in=scopes)
            access_ranges = set(access_ranges.values_list('key', flat=True))
            difference = access_ranges.symmetric_difference(scopes)
            if len(difference) != 0:
                raise InvalidScope("""Following access ranges do not
                    exist: %s""" % ', '.join(difference))
    
    def check_redirect_uri(self):
        if self.redirect_uri is None:
            raise MissingRedirectURI('No redirect_uri to send response.')
        if not absolute_http_url_re.match(self.redirect_uri):
            raise MissingRedirectURI('Absolute redirect_uri required.')
    
    def error_redirect(self):
        self.check_redirect_uri()
        if self.error is not None:
            e = self.error
        else:
            e = AccessDenied("Access Denied.")
        qs = {'error': e.error, 'error_description': u'%s' % e.message}
        if self.state is not None:
            qs['state'] = self.state
        redirect_uri = add_parameters(self.redirect_uri, qs)
        return HttpResponseRedirect(redirect_uri)
    
    def grant_redirect(self):
        if not self.valid:
            raise UnvalidatedRequest("""This request is invalid or has not 
                been validated.""")
        if self.user.is_authenticated():
            qs = {}
            frag = {}
            response_type = RESPONSE_TYPES[self.response_type]
            if response_type in [CODE, CODE_AND_TOKEN]:
                code = Code.objects.create(
                    user=self.user, 
                    client=self.client,
                    redirect_uri=self.redirect_uri,
                    scope=self.scope)
                qs['code'] = code.key
            if response_type in [TOKEN, CODE_AND_TOKEN]:
                access_token = AccessToken.objects.create(
                    user=self.user,
                    client=self.client)
                frag['access_token'] = access_token.token
                frag['expires_in'] = ACCESS_TOKEN_EXPIRATION
                frag['scope'] = self.scope
            if self.state is not None:
                qs['state'] = self.state
            redirect_uri = add_parameters(self.redirect_uri, qs)
            redirect_uri = add_fragments(redirect_uri, frag)
            return HttpResponseRedirect(redirect_uri)
        else:
            raise UnauthenticatedUser("""Django user object associated with the
                request is not authenticated.""")
