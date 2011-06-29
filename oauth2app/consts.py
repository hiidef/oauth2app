#-*- coding: utf-8 -*-


from django.conf import settings


# Length of the client key.
CLIENT_KEY_LENGTH = getattr(settings, "OAUTH2_CLIENT_KEY_LENGTH", 30)
# Length of the client secret.
CLIENT_SECRET_LENGTH = getattr(settings, "OAUTH2_CLIENT_SECRET_LENGTH", 30)
# Length of the code key.
CODE_KEY_LENGTH = getattr(settings, "OAUTH2_CODE_KEY_LENGTH", 30)
# Length of the access token.
ACCESS_TOKEN_LENGTH = getattr(settings, "OAUTH2_ACCESS_TOKEN_LENGTH", 10)
# Length of the refresh token.
REFRESH_TOKEN_LENGTH = getattr(settings, "OAUTH2_REFRESH_TOKEN_LENGTH", 10)
# Issue refreshable tokens.
REFRESHABLE = getattr(settings, "OAUTH2_REFRESHABLE", True)
# Number of seconds in which an authorization code should expire.
CODE_EXPIRATION = getattr(settings, "OAUTH2_CODE_EXPIRATION", 120)
# Number of seconds in which an access token should expire.
ACCESS_TOKEN_EXPIRATION = getattr(settings, "OAUTH2_ACCESS_TOKEN_EXPIRATION", 3600)
# Send MAC style authentication parameters. See http://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-00
MAC_KEY = getattr(settings, "OAUTH2_MAC_KEY", True)
# Authentication realm
REALM = getattr(settings, "OAUTH2_REALM", "")