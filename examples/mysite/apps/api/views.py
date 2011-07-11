#-*- coding: utf-8 -*-


from oauth2app.authenticate import JSONAuthenticator, AuthenticationException
from oauth2app.models import AccessRange

def date_joined(request):
    scope = AccessRange.objects.get(key="date_joined")
    authenticator = JSONAuthenticator(request, scope=scope)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response({
        "date_joined":str(authenticator.user.date_joined)})
    
    
def last_login(request):
    scope = AccessRange.objects.get(key="last_login")
    authenticator = JSONAuthenticator(request, scope=scope)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    data = {"date_joined":str(request.user.date_joined)}
    return authenticator.response({
        "last_login":str(authenticator.user.last_login)})


def email(request):
    authenticator = JSONAuthenticator(request)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.response({"email":authenticator.user.email})    
