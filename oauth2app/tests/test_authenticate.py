from unittest import TestCase

from nose.tools import assert_raises

from oauth2app.authenticate import Authenticator


class AuthenticateTestCase(TestCase):
    def setUp(self):
        self.authenticator = Authenticator(authentication_method='')
        class Request(object): pass
        self.request = Request()

    def test_invalid_request(self):
        self.request.bearer_token = 'herp'
        assert_raises(self.authenticator.validate, 'self.request')

