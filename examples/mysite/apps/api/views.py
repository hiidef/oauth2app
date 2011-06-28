#-*- coding: utf-8 -*-


from oauth2app.authenticate import Authenticator, AuthenticationException
from oauth2app.models import AccessRange

def date_joined(request):
    scope = AccessRange.objects.get(key="date_joined")
    authenticator = Authenticator(request, scope=scope)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.grant_response({
        "date_joined":str(request.user.date_joined)})
    
    
def last_login(request):
    scope = AccessRange.objects.get(key="last_login")
    authenticator = Authenticator(request, scope=scope)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    data = {"date_joined":str(request.user.date_joined)}
    return authenticator.grant_response({
        "last_login":str(request.user.last_login)})


def email(request):
    authenticator = Authenticator(request)
    try:
        authenticator.validate()
    except AuthenticationException:
        return authenticator.error_response()
    return authenticator.grant_response({"email":request.user.email})    
