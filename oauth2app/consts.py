#-*- coding: utf-8 -*-


"""OAuth 2.0 Default Values."""


from django.conf import settings
from .exceptions import OAuth2Exception


# Length of the client key.
CLIENT_KEY_LENGTH = getattr(settings, "OAUTH2_CLIENT_KEY_LENGTH", 30)
# Length of the client secret.
CLIENT_SECRET_LENGTH = getattr(settings, "OAUTH2_CLIENT_SECRET_LENGTH", 30)
# Length of the code key.
CODE_KEY_LENGTH = getattr(settings, "OAUTH2_CODE_KEY_LENGTH", 30)
# Length of the MAC authentication key.
MAC_KEY_LENGTH = getattr(settings, "OAUTH2_MAC_KEY_LENGTH", 20)
# Length of the access token.
ACCESS_TOKEN_LENGTH = getattr(settings, "OAUTH2_ACCESS_TOKEN_LENGTH", 10)
# Length of the refresh token.
REFRESH_TOKEN_LENGTH = getattr(settings, "OAUTH2_REFRESH_TOKEN_LENGTH", 10)
# Issue refreshable tokens.
REFRESHABLE = getattr(settings, "OAUTH2_REFRESHABLE", True)
# Number of seconds in which an authorization code should expire.
CODE_EXPIRATION = getattr(settings, "OAUTH2_CODE_EXPIRATION", 120)
# Number of seconds in which an access token should expire.
ACCESS_TOKEN_EXPIRATION = getattr(
    settings, 
    "OAUTH2_ACCESS_TOKEN_EXPIRATION", 
    3600)
# Sends and accepts Bearer style authentication parameters 
# See http://tools.ietf.org/html/draft-ietf-oauth-saml2-bearer-03
# and http://tools.ietf.org/html/draft-ietf-oauth-v2-bearer-04
BEARER = 1
# Sends and accepts MAC style authentication parameters 
# See http://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-00
MAC = 2 
# Type of authentication to use. Bearer or MAC.
AUTHENTICATION_METHOD = getattr(
    settings, 
    "OAUTH2_AUTHENTICATION_METHOD", 
    BEARER)
if AUTHENTICATION_METHOD not in [BEARER, MAC]:
    raise OAuth2Exception("Possible values for OAUTH2_AUTHENTICATION_METHOD "
        "are oauth2app.consts.MAC and oauth2app.consts.BEARER")
# Authentication realm
REALM = getattr(settings, "OAUTH2_REALM", "")
# Grants token style fragments.
TOKEN = 1
# Grants code style parameters.
CODE = 2
# Grants both style parameters.
CODE_AND_TOKEN = CODE | TOKEN