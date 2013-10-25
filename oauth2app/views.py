from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView, View
from django.views.generic.base import TemplateResponseMixin


from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from django_conneg.views import HTMLView

from . import forms


class MissingRedirectURLView(TemplateView):
    template_name = 'oauth2app/missing-redirect-url.html'
    
class AuthorizeView(TemplateResponseMixin, View):
    template_name = 'oauth2app/authorize.html'
    
    missing_redirect_url_view = staticmethod(MissingRedirectURLView.as_view())

    @method_decorator(login_required)
    def dispatch(self, request):
        self.authorizer = Authorizer()
        try:
            self.authorizer.validate(request)
        except MissingRedirectURI, e:
            return self.missing_redirect_url_view(request)
        except AuthorizationException, e:
            # The request is malformed or invalid. Automatically
            # redirects to the provided redirect URL.
            return self.authorizer.error_redirect()
        return super(AuthorizeView, self).dispatch(request)
    
    def get_context_data(self):
        #import pdb;pdb.set_trace()
        return {'authorizer': self.authorizer,
                'access_ranges': self.authorizer.access_ranges,
                'client': self.authorizer.client,
                'form': forms.AuthorizeForm(self.request.POST or \
                                            self.request.GET or None)}

    def get(self, request):
        context = self.get_context_data()
        if self.authorizer.client.auto_authorize:
            return self.authorizer.grant_redirect()
        return self.render_to_response(context)

    def post(self, request):
        context = self.get_context_data()
        if context['form'].is_valid():
            if 'accept' in request.POST:
                return self.authorizer.grant_redirect()
            else:
                return self.authorizer.error_redirect()
        return HttpResponseBadRequest()
