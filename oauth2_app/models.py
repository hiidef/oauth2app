#-*- coding: utf-8 -*-


import time
from hashlib import sha512
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from .consts import *
from .lib.response import RESPONSE_CHOICES, CODE


class TimestampGenerator(object):

    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds


class KeyGenerator(object):
    
    def __init__(self, length):
        self.length = length
    
    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]


class Client(models.Model):
    
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)    
    key = models.CharField(
        unique=True, 
        max_length=CLIENT_KEY_LENGTH, 
        default=KeyGenerator(CLIENT_KEY_LENGTH))
    secret = models.CharField(
        unique=True, 
        max_length=CLIENT_SECRET_LENGTH, 
        default=KeyGenerator(CLIENT_SECRET_LENGTH))
    redirect_uri = models.URLField(null=True, blank=True)
    authorized_reponse_types = models.PositiveIntegerField(
        default=CODE)
    

class AccessRange(models.Model):
    
    # 255 max_length when unique with mysql
    key = models.CharField(unique=True, max_length=255) 
    description = models.TextField(blank=True)


class AccessToken(models.Model):
    
    token = models.CharField(
        max_length=ACCESS_TOKEN_LENGTH, 
        default=KeyGenerator(ACCESS_TOKEN_LENGTH))
    refresh_token = models.CharField(
        blank=True, 
        null=True, 
        max_length=REFRESH_TOKEN_LENGTH, 
        default=KeyGenerator(REFRESH_TOKEN_LENGTH))
    issue = models.PositiveIntegerField(
        editable=False, 
        default=TimestampGenerator())
    expire = models.PositiveIntegerField(
        default=TimestampGenerator(ACCESS_TOKEN_EXPIRATION))
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User, related_name='access_tokens')
    scope = models.TextField(null=True, blank=True)
    refreshable = models.BooleanField(default=REFRESHABLE)


class Code(models.Model):
    
    key = models.CharField(
        max_length=CODE_KEY_LENGTH, 
        default=KeyGenerator(CODE_KEY_LENGTH))
    client = models.ForeignKey(Client)
    issue = models.PositiveIntegerField(
        editable=False, 
        default=TimestampGenerator())
    expire = models.PositiveIntegerField(
        default=TimestampGenerator(CODE_EXPIRATION))
    redirect_uri = models.URLField(null=True, blank=True)
    scope = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User, related_name='codes')

