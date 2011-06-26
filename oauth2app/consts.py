#-*- coding: utf-8 -*-


from django.conf import settings


CLIENT_KEY_LENGTH = getattr(settings, "OAUTH2_CLIENT_KEY_LENGTH", 30)
CLIENT_SECRET_LENGTH = getattr(settings, "OAUTH2_CLIENT_SECRET_LENGTH", 30)
CODE_KEY_LENGTH = getattr(settings, "OAUTH2_CODE_KEY_LENGTH", 30)
ACCESS_TOKEN_LENGTH = getattr(settings, "OAUTH2_ACCESS_TOKEN_LENGTH", 10)
REFRESH_TOKEN_LENGTH = getattr(settings, "OAUTH2_REFRESH_TOKEN_LENGTH", 10)
REFRESHABLE = getattr(settings, "OAUTH2_REFRESHABLE", True)
CODE_EXPIRATION = getattr(settings, "OAUTH2_CODE_EXPIRATION", 120)
ACCESS_TOKEN_EXPIRATION = getattr(settings, "OAUTH2_ACCESS_TOKEN_EXPIRATION", 3600)
MAC_KEY = getattr(settings, "OAUTH2_MAC_KEY", True)