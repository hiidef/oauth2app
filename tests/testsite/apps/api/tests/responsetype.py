#-*- coding: utf-8 -*-

from base64 import b64encode
from urlparse import urlparse, parse_qs
from urllib import urlencode
from django.utils import unittest
from django.test.client import Client as DjangoTestClient
from django.contrib import auth
from django.contrib.auth.models import User
from oauth2app.models import Client


USER_USERNAME = "testuser"
USER_PASSWORD = "testpassword"
USER_EMAIL = "user@example.com"
USER_FIRSTNAME = "Foo"
USER_LASTNAME = "Bar"
CLIENT_USERNAME = "client"
CLIENT_EMAIL = "client@example.com"
REDIRECT_URI = "http://example.com/callback"


class ResponseTypeTestCase(unittest.TestCase):
    
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
    
    def test_00_code(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)      
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"code"}
        response = user.get("/oauth2/authorize_code?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("code" in qs) 
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_code?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("error" in qs)
                
    def test_01_token(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)      
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_token?%s" % urlencode(parameters))
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("access_token" in fs)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"code"}
        response = user.get("/oauth2/authorize_token?%s" % urlencode(parameters))
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("error" in fs)

    def test_02_token_mac(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)      
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_token_mac?%s" % urlencode(parameters))
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("mac_key" in fs)

    def test_03_code_and_token(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)      
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"code"}
        response = user.get("/oauth2/authorize_code_and_token?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("code" in qs)
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("access_token" not in fs)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"token"}
        response = user.get("/oauth2/authorize_code_and_token?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("code" not in qs)
        fs = parse_qs(urlparse(response['location']).fragment)
        self.assertTrue("access_token" in fs)
        
    def test_04_invalid_response_type(self):
        user = DjangoTestClient()
        user.login(username=USER_USERNAME, password=USER_PASSWORD)
        parameters = {
            "client_id":self.client_application.key,
            "redirect_uri":REDIRECT_URI,
            "response_type":"blah"}
        response = user.get("/oauth2/authorize_code_and_token?%s" % urlencode(parameters))
        qs = parse_qs(urlparse(response['location']).query)
        self.assertTrue("error" in qs)   
