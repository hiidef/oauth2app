#-*- coding: utf-8 -*-


"""OAuth 2.0 Django Models"""


import time
from hashlib import sha512
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.db.models import get_model
from django.contrib.auth.models import UNUSABLE_PASSWORD
from .consts import CLIENT_KEY_LENGTH, CLIENT_SECRET_LENGTH
from .consts import ACCESS_TOKEN_LENGTH, REFRESH_TOKEN_LENGTH
from .consts import ACCESS_TOKEN_EXPIRATION, MAC_KEY_LENGTH, REFRESHABLE
from .consts import CODE_KEY_LENGTH, CODE_EXPIRATION


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
SCOPE_USER_PREFIX = getattr(settings, 'AUTH_OAUTH_SCOPE_USER_PREFIX', 'o2s_')

class TimestampGenerator(object):
    """Callable Timestamp Generator that returns a UNIX time integer.

    **Kwargs:**

    * *seconds:* A integer indicating how many seconds in the future the
      timestamp should be. *Default 0*

    *Returns int*
    """
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds


class KeyGenerator(object):
    """Callable Key Generator that returns a random keystring.

    **Args:**

    * *length:* A integer indicating how long the key should be.

    *Returns str*
    """
    def __init__(self, length):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]


class Client(models.Model):
    """Stores client authentication data.

    **Args:**

    * *name:* A string representing the client name.
    * *user:* A Django User object representing the client
       owner.

    **Kwargs:**

    * *description:* A string representing the client description.
      *Default None*
    * *key:* A string representing the client key. *Default 30 character
      random string*
    * *secret:* A string representing the client secret. *Default 30 character
      random string*
    * *redirect_uri:* A string representing the client redirect_uri.
      *Default None*
    * *auto_authorize:* Don't ask the user to confirm authorization.

    """
    name = models.CharField(max_length=256)
    user = models.ForeignKey(AUTH_USER_MODEL)
    description = models.TextField(null=True, blank=True)
    key = models.CharField(
        unique=True,
        max_length=CLIENT_KEY_LENGTH,
        default=KeyGenerator(CLIENT_KEY_LENGTH),
        db_index=True)
    secret = models.CharField(
        unique=True,
        max_length=CLIENT_SECRET_LENGTH,
        default=KeyGenerator(CLIENT_SECRET_LENGTH))
    redirect_uri = models.URLField(null=True)
    auto_authorize = models.BooleanField()

    all_scopes_allowable = models.BooleanField()
    allowable_scopes = models.ManyToManyField('AccessRange', blank=True)


class AccessRange(models.Model):
    """Stores access range data, also known as scope.

    **Args:**

    * *key:* A string representing the access range scope. Used in access
      token requests.

    **Kwargs:**

    * *description:* A string representing the access range description.
      *Default None*

    """
    key = models.CharField(unique=True, max_length=255, db_index=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    permission_user = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True,
                                        help_text="An auto-created user whose permissions this scope allows access to.")
    ttl = models.BigIntegerField(null=True, blank=True,
                                 help_text="Number of seconds before this scope is removed from an access token.")

    def save(self, *args, **kwargs):
        if not self.permission_user:
            user_model = get_model(*AUTH_USER_MODEL.split('.'))
            self.permission_user = user_model.objects.create(
                username=SCOPE_USER_PREFIX + uuid4().hex[:16],
                first_name='OAuth2 permissions granted by',
                last_name=self.key,
                password=UNUSABLE_PASSWORD)
        super(AccessRange, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.key

class AccessToken(models.Model):
    """Stores access token data.

    **Args:**

    * *client:* A oauth2app.models.Client object
    * *user:* A Django User object

    **Kwargs:**

    * *token:* A string representing the access key token. *Default 10
      character random string*
    * *refresh_token:* A string representing the access key token. *Default 10
      character random string*
    * *mac_key:* A string representing the MAC key. *Default None*
    * *expire:* A positive integer timestamp representing the access token's
      expiration time.
    * *scope:* A list of oauth2app.models.AccessRange objects. *Default None*
    * *refreshable:* A boolean that indicates whether this access token is
      refreshable. *Default False*

    """
    client = models.ForeignKey(Client)
    user = models.ForeignKey(AUTH_USER_MODEL)
    token = models.CharField(
        unique=True,
        max_length=ACCESS_TOKEN_LENGTH,
        default=KeyGenerator(ACCESS_TOKEN_LENGTH),
        db_index=True)
    refresh_token = models.CharField(
        unique=True,
        blank=True,
        null=True,
        max_length=REFRESH_TOKEN_LENGTH,
        default=KeyGenerator(REFRESH_TOKEN_LENGTH),
        db_index=True)
    mac_key = models.CharField(
        unique=True,
        blank=True,
        null=True,
        max_length=MAC_KEY_LENGTH,
        default=None)
    issue = models.PositiveIntegerField(
        editable=False,
        default=TimestampGenerator())
    expire = models.PositiveIntegerField(
        default=TimestampGenerator(ACCESS_TOKEN_EXPIRATION))
    scope = models.ManyToManyField(AccessRange)
    refreshable = models.BooleanField(default=REFRESHABLE)


class Code(models.Model):
    """Stores authorization code data.

    **Args:**

    * *client:* A oauth2app.models.Client object
    * *user:* A Django User object

    **Kwargs:**

    * *key:* A string representing the authorization code. *Default 30
      character random string*
    * *expire:* A positive integer timestamp representing the access token's
      expiration time.
    * *redirect_uri:* A string representing the redirect_uri provided by the
      requesting client when the code was issued. *Default None*
    * *scope:* A list of oauth2app.models.AccessRange objects. *Default None*

    """
    client = models.ForeignKey(Client)
    user = models.ForeignKey(AUTH_USER_MODEL)
    key = models.CharField(
        unique=True,
        max_length=CODE_KEY_LENGTH,
        default=KeyGenerator(CODE_KEY_LENGTH),
        db_index=True)
    issue = models.PositiveIntegerField(
        editable=False,
        default=TimestampGenerator())
    expire = models.PositiveIntegerField(
        default=TimestampGenerator(CODE_EXPIRATION))
    redirect_uri = models.URLField(null=True)
    scope = models.ManyToManyField(AccessRange)


class MACNonce(models.Model):
    """Stores Nonce strings for use with MAC Authentication.

    **Args:**

    * *access_token:* A oauth2app.models.AccessToken object
    * *nonce:* A unique nonce string.

    """
    access_token = models.ForeignKey(AccessToken)
    nonce = models.CharField(max_length=30, db_index=True)
