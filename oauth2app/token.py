#-*- coding: utf-8 -*-


from base64 import b64encode, b64decode
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from simplejson import dumps
from .exceptions import OAuth2Exception
from .consts import ACCESS_TOKEN_EXPIRATION, REFRESH_TOKEN_LENGTH, MAC_KEY
from .lib.uri import normalize
from .models import Client, AccessRange, Code, AccessToken, TimestampGenerator, KeyGenerator


class AccessTokenException(OAuth2Exception):
    """Access Token exception base class."""
    pass


class UnvalidatedRequest(OAuth2Exception):
    """The method requested requires a validated request to continue."""
    pass


class InvalidRequest(AccessTokenException):
    """The request is missing a required parameter, includes an
    unsupported parameter or parameter value, repeats a
    parameter, includes multiple credentials, utilizes more
    than one mechanism for authenticating the client, or is
    otherwise malformed."""
    error = 'invalid_request'


class InvalidClient(AccessTokenException):
    """Client authentication failed (e.g. unknown client, no
    client credentials included, multiple client credentials
    included, or unsupported credentials type)."""
    error = 'invalid_client'


class UnauthorizedClient(AccessTokenException):
    """The client is not authorized to request an authorization
    code using this method."""
    error = 'unauthorized_client'


class InvalidGrant(AccessTokenException):
    """The provided authorization grant is invalid, expired,
    revoked, does not match the redirection URI used in the
    authorization request, or was issued to another client."""
    error = 'invalid_grant'


class UnsupportedGrantType(AccessTokenException):
    """The authorization grant type is not supported by the
    authorization server."""
    error = 'unsupported_grant_type'


class InvalidScope(AccessTokenException):
    """The requested scope is invalid, unknown, malformed, or
    exceeds the scope granted by the resource owner."""
    error = 'invalid_scope'


@csrf_exempt
def handler(request):
    """Django view that handles the token endpoint. Returns a JSON formatted
    authorization code.

    **Args:**

    * *request:* Django HttpRequest object.

    """
    token_generator = TokenGenerator(request)
    try:
        token_generator.validate()
    except AccessTokenException, e:
        return token_generator.error_response()
    return token_generator.grant_response()


class TokenGenerator(object):
    """Token access handler. Validates authorization codes, refresh tokens,
    username/password pairs, and generates a JSON formatted authorization code.

    **Args:**

    * *request:* Django HttpRequest object."""

    valid = False
    code = None
    client = None
    access_token = None
    user = None
    error = None

    def __init__(self, request, scope=None):
        if scope is None:
            self.authorized_scope = None
        elif isinstance(scope, AccessRange):
            self.authorized_scope = set([scope.key])
        else:
            self.authorized_scope = set([x.key for x in scope])
        self.grant_type = request.REQUEST.get('grant_type')
        self.client_id = request.REQUEST.get('client_id')
        self.client_secret = request.POST.get('client_secret')
        self.scope = request.REQUEST.get('scope')
        # authorization_code, see 4.1.3.  Access Token Request
        self.code_key = request.REQUEST.get('code')
        self.redirect_uri = request.REQUEST.get('redirect_uri')
        # refresh_token, see 6.  Refreshing an Access Token
        self.refresh_token = request.REQUEST.get('refresh_token')
        # password, see 4.3.2. Access Token Request
        self.email = request.REQUEST.get('email')
        self.username = request.REQUEST.get('username')
        self.password = request.REQUEST.get('password')
        # Optional json callback
        self.callback = request.REQUEST.get('callback')
        self.request = request

    def validate(self):
        """Validate the request. Raises an AccessTokenException if the
        request fails authorization.

        *Returns None*"""
        try:
            self._validate()
        except AccessTokenException, e:
            self.error = e
            raise e
        self.valid = True

    def _validate(self):
        # Check response type
        if self.grant_type is None:
            raise InvalidRequest('No grant_type provided.')
        if self.grant_type not in [
                "authorization_code",
                "refresh_token",
                "password",
                "client_credentials"]:
            raise UnsupportedGrantType('No such grant type: %s' % self.grant_type)
        if self.client_id is None:
            raise InvalidRequest('No client_id')
        try:
            self.client = Client.objects.get(key=self.client_id)
        except Client.DoesNotExist:
            raise InvalidClient("client_id %s doesn't exist" % self.client_id)
        # Scope
        if self.scope is not None:
            scopes = set(self.scope.split())
            access_ranges = AccessRange.objects.filter(key__in=scopes)
            access_ranges = set(access_ranges.values_list('key', flat=True))
            difference = access_ranges.symmetric_difference(scopes)
            if len(difference) != 0:
                raise InvalidScope("Following access ranges doesn't exist: %s" % ', '.join(difference))
        if self.grant_type == "authorization_code":
            self._validate_authorization_code()
        elif self.grant_type == "refresh_token":
            self._validate_refresh_token()
        elif self.grant_type == "password":
            self._validate_password()
        elif self.grant_type == "client_credentials":
            self._validate_client_credentials()
        else:
            raise UnsupportedGrantType('Unable to validate grant type.')

    def _validate_access_credentials(self):
        """Validate the request's access credentials."""
        if self.client_secret is None and "HTTP_AUTHORIZATION" in self.request.META:
            auth, value = self.request.META["HTTP_AUTHORIZATION"].split()[0:2]
            if auth.lower() == "basic":
                if value != b64encode("%s:%s" % (self.client.key, self.client.secret)):
                    raise InvalidClient('Client authentication failed.')
            else:
                raise InvalidClient('Client authentication failed.')
        elif self.client_secret != self.client.secret:
            raise InvalidClient('Client authentication failed.')

    def _validate_client_credentials(self):
        """Validate a client_credentials request."""
        self._validate_access_credentials()

    def _validate_authorization_code(self):
        """Validate an authorization_code request."""
        if self.code_key is None:
            raise InvalidRequest('No code_key provided')
        self._validate_access_credentials()
        try:
            self.code = Code.objects.get(key=self.code_key)
        except Code.DoesNotExist:
            raise InvalidRequest('No such code: %s' % self.code_key)
        now = TimestampGenerator()()
        if self.code.expire < now:
            raise InvalidGrant("Provided code is expired")
        self.scope = ' '.join([x.key for x in self.code.scope.all()])
        if self.redirect_uri is None:
            raise InvalidRequest('No redirect_uri')
        if normalize(self.redirect_uri) != normalize(self.code.redirect_uri):
            raise InvalidRequest("redirect_uri doesn't match")

    def _validate_password(self):
        """Validate a password request."""
        if self.username is None and self.email is None:
            raise InvalidRequest('No username')
        if self.password is None:
            raise InvalidRequest('No password')
        if self.scope is not None:
            scopes = set(self.scope.split())
            access_ranges = AccessRange.objects.filter(key__in=scopes)
            access_ranges = set(access_ranges.values_list('key', flat=True))
            difference = access_ranges.symmetric_difference(scopes)
            if len(difference) != 0:
                raise InvalidScope("""Following access ranges do not
                    exist: %s""" % ', '.join(difference))
            if self.authorized_scope is not None:
                new_scope = scopes - self.authorized_scope
                if len(new_scope) > 0:
                    raise InvalidScope("""Invalid scope request: %s""" % list(new_scope))
        if "HTTP_AUTHORIZATION" in self.request.META:
            auth, value = self.request.META["HTTP_AUTHORIZATION"].split()[0:2]
            if auth.lower() == "basic":
                if value != b64encode("%s:%s" % (self.client.key, self.client.secret)):
                    raise InvalidClient('Client authentication failed.')
            else:
                raise InvalidClient('Client authentication failed.')
        else:
            raise InvalidClient('Client authentication failed.')
        if self.username is not None:
            user = authenticate(username=self.username, password=self.password)
        else:
            user = authenticate(email=self.email, password=self.password)
        if user is not None:
            if not user.is_active:
                raise InvalidRequest('Inactive user.')
        else:
            raise InvalidRequest('User authentication failed.')
        self.user = user

    def _validate_refresh_token(self):
        """Validate a refresh token request."""
        if self.refresh_token is None:
            raise InvalidRequest('No refresh_token')
        try:
            self.access_token = AccessToken.objects.get(refresh_token=self.refresh_token)
        except AccessToken.DoesNotExist:
            raise InvalidRequest('No such refresh token: %s' % self.refresh_token)
        self._validate_access_credentials()
        if self.scope is not None:
            access_ranges = set([x.key for x in self.access_token.scope.all()])
            scopes = set(self.scope.split())
            new_scope = scopes - access_ranges
            if len(new_scope) > 0:
                raise InvalidScope("Refresh request requested scopes beyond"
                "initial grant: %s" % new_scope)

    def error_response(self):
        """In the event of an error, return a Django HttpResponse
        with the appropriate JSON encoded error parameters.

        *Returns HttpResponse*"""
        if self.error is not None:
            e = self.error
        else:
            e = InvalidRequest("Access Denied.")
        data = {'error': e.error, 'error_description': u'%s' % e.message}
        json_data = dumps(data)
        if self.callback is not None:
            json_data = "%s(%s);" % (self.callback, json_data)
            return HttpResponse(
                content=json_data,
                content_type='application/json')
        else:
            response = HttpResponse(
                content=json_data,
                content_type='application/json')
            if isinstance(self.error, InvalidClient):
                response.status_code = 401
            else:
                response.status_code = 400
            return response

    def grant_response(self):
        """Returns a JSON formatted authorization code."""
        if not self.valid:
            raise UnvalidatedRequest("This request is invalid or has not been validated.")
        if self.grant_type == "authorization_code":
            access_token = self._get_authorization_code_token()
        elif self.grant_type == "refresh_token":
            access_token = self._get_refresh_token()
        elif self.grant_type == "password":
            access_token = self._get_password_token()
        elif self.grant_type == "client_credentials":
            access_token = self._get_client_credentials_token()
        data = {
            'access_token': access_token.token,
            'expire_in': ACCESS_TOKEN_EXPIRATION}
        # if MAC_KEY:
        #     data["mac_key"] = "hmac-sha-256"
        #     data["mac_algorithm"] = "hmac-sha-256"
        if access_token.refreshable:
            data['refresh_token'] = access_token.refresh_token
        if self.scope:
            data['scope'] = ' '.join(self.scope)
        json_data = dumps(data)
        if self.callback is not None:
            json_data = "%s(%s);" % (self.callback, json_data)
        response = HttpResponse(
            content=json_data,
            content_type='application/json')
        response['Cache-Control'] = 'no-store'
        return response

    def _get_authorization_code_token(self):
        access_token = AccessToken.objects.create(
            user=self.code.user,
            client=self.client)
        scopes = set(self.scope.split())
        access_ranges = list(AccessRange.objects.filter(key__in=scopes))
        access_token.scope = access_ranges
        access_token.save()
        self.code.delete()
        return access_token

    def _get_password_token(self):
        access_token = AccessToken.objects.create(
            user=self.user,
            client=self.client)
        scopes = set(self.scope.split())
        access_ranges = list(AccessRange.objects.filter(key__in=scopes))
        access_token.scope = access_ranges
        access_token.save()
        return access_token

    def _get_refresh_token(self):
        self.access_token.refresh_token = KeyGenerator(REFRESH_TOKEN_LENGTH)()
        self.access_token.expire = TimestampGenerator(ACCESS_TOKEN_EXPIRATION)()
        scopes = set(self.scope.split())
        access_ranges = list(AccessRange.objects.filter(key__in=scopes))
        self.access_token.scope = access_ranges
        self.access_token.save()
        return self.access_token

    def _get_client_credentials_token(self):
        access_token = AccessToken.objects.create(
            user=self.client.user,
            client=self.client,
            scope=self.scope)
        scopes = set(self.scope.split())
        access_ranges = list(AccessRange.objects.filter(key__in=scopes))
        self.access_token.scope = access_ranges
        return self.access_token



