#-*- coding: utf-8 -*-

"""OAuth 2.0 Django Models"""

import datetime
from hashlib import sha512
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from .consts import CLIENT_KEY_LENGTH, CLIENT_SECRET_LENGTH
from .consts import ACCESS_TOKEN_LENGTH, REFRESH_TOKEN_LENGTH
from .consts import ACCESS_TOKEN_EXPIRATION, MAC_KEY_LENGTH, REFRESHABLE
from .consts import CODE_KEY_LENGTH, CODE_EXPIRATION

# helper to generate 512 bit sha key
key_gen = lambda length: sha512(uuid4().hex).hexdigest()[0:length]


class Client(models.Model):
    """Stores client authentication data.

    **Args:**

    * *name:* A string representing the client name.
    * *user:* A django.contrib.auth.models.User object representing the client
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

    """
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User)

    description = models.TextField(null=True, blank=True)
    # 30 character random string, default pass in callable
    key = models.CharField(unique=True, max_length=CLIENT_KEY_LENGTH,
        default=lambda: key_gen(CLIENT_KEY_LENGTH), db_index=True)
    # 30 character random string, default pass in callable
    secret = models.CharField(unique=True, max_length=CLIENT_SECRET_LENGTH,
        default=lambda: key_gen(CLIENT_SECRET_LENGTH))
    redirect_uri = models.URLField(null=True)

    __unicode__ = lambda self: "%s" % self.name


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
    description = models.TextField(blank=True)

    __unicode__ = lambda self: "%s" % self.key


class AccessToken(models.Model):
    """Stores access token data.

    **Args:**

    * *client:* A oauth2app.models.Client object
    * *user:* A django.contrib.auth.models.User object

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
    user = models.ForeignKey(User)
    # random string representing access key token
    token = models.CharField(unique=True, max_length=ACCESS_TOKEN_LENGTH,
        default=lambda: key_gen(ACCESS_TOKEN_LENGTH), db_index=True)
    refresh_token = models.CharField(unique=True, blank=True, null=True, db_index=True,
        max_length=REFRESH_TOKEN_LENGTH, default=lambda: key_gen(REFRESH_TOKEN_LENGTH))
    mac_key = models.CharField(unique=True, blank=True, null=True,
        max_length=MAC_KEY_LENGTH, default=None)
    # auto_now_add defaults to now() when created
    issue = models.DateTimeField(auto_now_add=True, editable=False)
    # default now + ACCESS_TOKEN_EXPIRATION, need to pass callable function
    expire = models.DateTimeField(editable=False, default=lambda: 
        datetime.datetime.now() + datetime.timedelta(seconds=ACCESS_TOKEN_EXPIRATION)) 

    scope = models.ManyToManyField(AccessRange)
    refreshable = models.BooleanField(default=REFRESHABLE)

    __unicode__ = lambda self: "%s (%s)" % (self.client, self.user)


class Code(models.Model):
    """Stores authorization code data.

    **Args:**

    * *client:* A oauth2app.models.Client object
    * *user:* A django.contrib.auth.models.User object

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
    user = models.ForeignKey(User)
    key = models.CharField(unique=True, max_length=CODE_KEY_LENGTH,
        default=lambda: key_gen(CODE_KEY_LENGTH), db_index=True)
    # auto_now_add defaults to now() when created
    issue = models.DateTimeField(auto_now_add=True, editable=False)
    # default now + ACCESS_TOKEN_EXPIRATION, need to pass callable function
    expire = models.DateTimeField(editable=False, default=lambda: 
        datetime.datetime.now() + datetime.timedelta(seconds=CODE_EXPIRATION)) 

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
