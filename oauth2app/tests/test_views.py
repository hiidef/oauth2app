# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import RequestFactory

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from oauth2app import urls
from oauth2app.models import Client
from oauth2app.views import AuthorizeView
from oauth2app.authorize import MissingRedirectURI

def patch_request(request):
    """
    Fakes a session dict-like and a dummy user
    """
    request.session = {}
    request.user = User()
    return request


class TestAuthorizeViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = AuthorizeView.as_view()
        self.url = reverse('oauth2app_authorize')
        self.redirect_uri = 'http://example.com/'
        self.client_user = User.objects.create(username='ClientUser')
        self.client = Client.objects.create(
            user=self.client_user,
            name='test client',
            redirect_uri=self.redirect_uri,
        )

    def missing_uri(self):
        # GET request with no redirect_uri data, should raise MissingRedirectURI
        request = patch_request(self.factory.get(self.url))
        with self.assertRaises(MissingRedirectURI):
            response = self.view(request)

    def test_render(self):
        request = patch_request(self.factory.get(self.url, {
            'redirect_uri': self.redirect_uri,
            'client_id': self.client.key,
            'response_type': 'code',
        }))
        response = self.view(request)
        self.assertEquals(response.status_code, 200)

    def test_invalid_request(self):
        request = patch_request(self.factory.post(self.url, {
            'redirect_uri': self.redirect_uri,
        }))
        response = self.view(request)
        self.assertTrue(response['Location'].startswith(self.redirect_uri))

    def test_declined(self):
        request = patch_request(self.factory.post(self.url, {
            'connect': 'nooo',
            'redirect_uri': self.redirect_uri,
        }))
        response = self.view(request)
        self.assertTrue(response['Location'].startswith(self.redirect_uri))

    def _test_success(self):
        # create client user
        # create client
        # create customer user
        user = User.objects.create(username='User')
        # run view with client id
        request = patch_request(self.factory.post(self.url, {
            'connect': 'yes',
            'redirect_uri': self.redirect_uri,
            'client_id': self.client.key,
        }))
        authorizer = Authorizer()
        authorize_endpoint = authorizer.validate(request)
        # Check if token existe for customer user and client

