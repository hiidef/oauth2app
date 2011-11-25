#-*- coding: utf-8 -*-

from django.utils import unittest
from oauth2app.exceptions import OAuth2Exception
from oauth2app.authorize import Authorizer
from oauth2app.authenticate import Authenticator

class ConfigTestCase(unittest.TestCase):
    
    def test_00_authorize(self):
        self.assertRaises(OAuth2Exception, Authorizer, response_type=-1)
        self.assertRaises(OAuth2Exception, Authorizer, authentication_method=-1)

    def test_01_authenticate(self):
        self.assertRaises(OAuth2Exception, Authenticator, authentication_method=-1)
    