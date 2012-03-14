#-*- coding: utf-8 -*-


from uni_form.helpers import FormHelper, Submit, Reset
from oauth2app.views import AuthorizeView

class CustomAuthorizeView(AuthorizeView):
    def get_context_data(self, **kwargs):
        ctx = super(CustomAuthorizeView, self).get_context_data(**kwargs)

        # Django Uni-Form helper for pretty rendering
        helper = FormHelper()
        no_submit = Submit('connect','No')
        helper.add_input(no_submit)
        yes_submit = Submit('connect', 'Yes')
        helper.add_input(yes_submit)
        helper.form_action = '/oauth2/authorize?%s' % self.authorizer.query_string
        helper.form_method = 'POST'
        ctx['helper'] = helper
        return ctx
