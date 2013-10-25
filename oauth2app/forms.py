from django import forms

class AuthorizeForm(forms.Form):
    redirect_uri = forms.CharField(widget=forms.HiddenInput)
    client_id = forms.CharField(widget=forms.HiddenInput)
    response_type = forms.CharField(widget=forms.HiddenInput)
    scope = forms.CharField(widget=forms.HiddenInput, required=False)