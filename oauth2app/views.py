# -*- coding: utf-8 -*-

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from oauth2app.forms import AuthorizeForm
from oauth2app.consts import CODE_AND_TOKEN
from oauth2app.authorize import Authorizer, AuthorizationException

class MissingRedirectUriView(TemplateView):
    template_name = 'oauth2app/missing_redirect_uri.html'


class AuthorizeView(FormView):
    form_class = AuthorizeForm
    authorizer_class = Authorizer
    template_name = 'oauth2app/authorize.html'
    invalid_form_message = 'Please check the values and try again'
    authorizer_accept = CODE_AND_TOKEN

    # The form's submit button must be named 'connect' and have a value
    # from YES_ANSWERS
    PROCESS_BUTTON = 'connect'
    YES_ANSWERS = ['yes', 'on']

    def get_authorizer(self):
        return self.authorizer_class(response_type=self.authorizer_accept)

    def authorizer_is_valid(self):
        try:
            self.authorizer.validate(self.request)
        except AuthorizationException, e:
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        self.authorizer = self.get_authorizer()

        if not self.authorizer_is_valid():
            return self.authorizer.error_redirect()

        return super(AuthorizeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form_action'] = '%s?%s' % (reverse('oauth2app_authorize'),
            self.authorizer.query_string)
        kwargs['client'] = self.authorizer.client
        kwargs['access_ranges'] = self.authorizer.access_ranges

        return super(AuthorizeView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """
        This method will be executed once the user has succesfully submitted
        the authorization form authorizing the app to access the resource
        """

        can_connect = self.request.POST.get(self.PROCESS_BUTTON, '') or ''
        if can_connect.lower() in self.YES_ANSWERS:
            return self.authorizer.grant_redirect()
        else:
            return self.authorizer.error_redirect()

    def form_invalid(self, form):
        """
        This method get invoked if the authorization form did was not
        valid or tampered with
        """

        self.set_invalid_message()
        return HttpResponseRedirect(self.get_invalid_form_url())

    def set_invalid_message(self):
        messages.error(request, self.invalid_form_message)

    def get_invalid_form_url(self):
        """
        In the case of a tampered form, redirect to the form view
        """
        return reverse('oauth2app_authorize')


