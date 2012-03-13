# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import RequestFactory

from django.contrib.auth.models import User

from oauth2app import urls
from oauth2app.models import Client
from oauth2app.views import AuthorizeView

def patch_request(request):
    request.session = {}
    request.user = User()

class TestAuthorizeViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = AuthorizeView.as_view()
        self.url = reverse('oauth2app:authorize', urlconf=urls)

    def test_render(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEquals(response.status_code, 200)

    def test_invalid_request(self):
        request = patch_request(self.factory.post(self.url, {}))
        response = self.view(request)
        authorizer = view.authorizer
        error_redirect = authorizer.error_redirect()['Location']
        self.assertRedirectsTo(response, error_redirect)

    def test_declined(self):
        request = patch_request(self.factory.post(self.url, {
            'connect': 'nooo'
        }))
        request.session = {}
        requesr.user = User(username='')
        response = self.view(request)
        authorizer = view.authorizer
        error_redirect = authorizer.error_redirect()['Location']
        self.assertRedirectsTo(response, error_redirect)

    def test_success(self):
        # create client user
        client_user = User.objects.create(username='ClientUser')
        # create client
        client_redirect_url = '/client/redirect/'
        client = Client.objects.create(
            user=client_user,
            name='test client'
            redirect_url=client_redirect_url
        )
        # create customer user
        user = User.objects.create(username='User')
        # run view with client id
        request = patch_request(self.factory.post(self.url, {
            'connect': 'yes'
        }))
        authorizer = Authorizer()
        authorize_endpoint = authorizer.validate(request)
        # Check if token existe for customer user and client

