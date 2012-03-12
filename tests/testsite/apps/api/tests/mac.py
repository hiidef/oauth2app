#-*- coding: utf-8 -*-

import json
from base64 import b64encode
from urlparse import urlparse, parse_qs
from urllib import urlencode
from django.utils import unittest
from django.contrib.auth.models import User
from oauth2app.models import Client
from django.test.client import Client as DjangoTestClient


USER_USERNAME = "testuser"
USER_PASSWORD = "testpassword"
USER_EMAIL = "user@example.com"
USER_FIRSTNAME = "Foo"
USER_LASTNAME = "Bar"
CLIENT_USERNAME = "client"
CLIENT_EMAIL = "client@example.com"
REDIRECT_URI = "http://example.com/callback"


class MACTestCase(unittest.TestCase):
    
    user = None
    client_holder = None
    client_application = None

    def setUp(self):
        self.user = User.objects.create_user(
            USER_USERNAME, 
            USER_EMAIL, 
            USER_PASSWORD)
        self.user.first_name = USER_FIRSTNAME
        self.user.last_name = USER_LASTNAME
        self.user.save()
        self.client = User.objects.create_user(CLIENT_USERNAME, CLIENT_EMAIL)
        self.client_application = Client.objects.create(    
            name="TestApplication", 
            user=self.client)
    
    def tearDown(self):
        self.user.delete()
        self.client.delete()
        self.client_application.delete()
    
    def test_00_mac(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)      
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"code"}
        response = user.get("/oauth2/authorize_mac?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        code = qs['code']
        client = DjangoTestClient()
        parameters = {
            "client_id":self.client_application.key,
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":REDIRECT_URI}
        basic_auth = b64encode("%s:%s" % (self.client_application.key, self.client_application.secret))
        response = client.get(
            "/oauth2/token_mac", 
            parameters, 
            HTTP_AUTHORIZATION="Basic %s" % basic_auth)
        token = json.loads(response.content)
        
