import httplib

from oauth2app.authenticate import Authenticator, AuthenticationException
from oauth2app.consts import REALM
from .backends import OAuth2ProxyUser

class OAuth2Middleware(object):
    def process_request(self, request):
        authenticator = Authenticator()
        #import pdb;pdb.set_trace()
        try:
            authenticator.validate(request)
        except AuthenticationException, e:
            if authenticator.bearer_token or authenticator.auth_type in ['bearer', 'mac']:
                return authenticator.error_response(content="You didn't authenticate.")
        else:
            request.user = OAuth2ProxyUser(authenticator.access_token)

    def process_response(self, request, response):
        user = getattr(request, 'user', None)
        if user and hasattr(user, 'scopes'):
            response['X-OAuth2-Scopes'] = ' '.join(user.scopes)

        if response.status_code == httplib.UNAUTHORIZED:
            authenticate = response.get('WWW-Authenticate', None)
            if 'Bearer realm="' not in authenticate:
                if authenticate:
                    authenticate = 'Bearer realm="%s", %s' % (REALM, authenticate)
                else:
                    authenticate = 'Bearer realm="%s"' % REALM
            response['WWW-Authenticate'] = authenticate

        return response
