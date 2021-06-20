import time
import datetime

from django.contrib import admin
from django.template.defaultfilters import timeuntil, timesince

from oauth2app.models import Client, AccessToken, AccessRange

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'description', 'key', 'redirect_uri')

class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'client_name', 'remaining', 'refreshable')
    
    def client_name(self, obj):
        return obj.client.name
    
    def remaining(self, obj):
        remaining = int(obj.expire - time.time())
        if remaining > 0:
            return timeuntil(datetime.datetime.fromtimestamp(obj.expire))
        else:
            return "expired {0} ago".format(timesince(datetime.datetime.fromtimestamp(obj.expire)))

class AccessRangeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(AccessRange, AccessRangeAdmin)
