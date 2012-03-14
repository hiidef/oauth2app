# -*- coding: utf-8 -*-

from django import forms

class AuthorizeForm(forms.Form):
    """ Basic authorization form, it does not contain any fields, as it is 
    only intended to be used as an "Accept" button authorizing the app
    to the resource """
    pass
