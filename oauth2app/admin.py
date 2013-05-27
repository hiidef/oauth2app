
from django.contrib import admin

from oauth2app.models import Client, AccessRange, AccessToken, Code, MACNonce


class ClientAdmin(admin.options.ModelAdmin):
    list_display = ('name', 'user', 'key', 'secret', 'redirect_uri')


class AccessRangeAdmin(admin.options.ModelAdmin):
    list_display = ('key', 'description')


class AccessTokenAdmin(admin.options.ModelAdmin):
    list_display = ('client', 'user', 'token', 'refresh_token', 
            'mac_key', 'issue', 'expire', 'refreshable')
    filter_horizontal = ['scope']


class CodeAdmin(admin.options.ModelAdmin):
    list_display = ('client', 'user', 'key', 'issue', 'expire', 
            'redirect_uri')
    filter_horizontal = ['scope']


class MACNonceAdmin(admin.options.ModelAdmin):
    list_display = ('access_token', 'nonce')


admin.site.register(Client, ClientAdmin)
admin.site.register(AccessRange, AccessRangeAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(MACNonce, MACNonceAdmin)
