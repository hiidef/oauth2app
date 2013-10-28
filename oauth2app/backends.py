"""
Authentication backend that uses AccessRange groups to filter access.
"""

from django.contrib.auth.models import User

class OAuth2ProxyUser(User):
    """
    A proxy in front of the actual User that restricts access based on
    AccessRange permission_users.
    """
    def __init__(self, access_token):
        self.access_token = access_token
        self.user, self.client = access_token.user, access_token.client

        scopes = list(access_token.scope.all())
        self.scopes = [scope.key for scope in scopes]
        self.scope_users = [scope.permission_user for scope in scopes
                            if scope.permission_user and scope.permission_user.is_active]

    fk = property(lambda self: self.user.fk)
    username = property(lambda self: self.user.username)
    first_name = property(lambda self: self.user.first_name)
    last_name = property(lambda self: self.user.last_name)
    is_active = property(lambda self: self.user.is_active)
    date_joined = property(lambda self: self.user.date_joined)

    # Only allow a client to act as staff or a superuser if one of its scopes
    # enables it to do so.
    @property
    def is_staff(self):
        return self.user.is_staff \
            and any(u.is_staff for u in self.scope_users)
    @property
    def is_superuser(self):
        return self.user.is_superuser \
            and any(u.is_superuser for u in self.scope_users)

    def get_all_permissions(self, obj=None):
        perms = set()
        for u in self.scope_users:
            perms |= u.get_all_permissions(obj)
        perms &= self.user.get_all_permissions(obj)
        return perms

    def has_perm(self, perm, obj=None):
        return self.user.has_perm(perm, obj) \
            and any(u.has_perm(perm, obj) for u in self.scope_users)

    def has_perms(self, perm_list, obj=None):
        return self.user.has_perms(perm_list, obj) \
            and any(u.has_perms(perm_list, obj) for u in self.scope_users)
