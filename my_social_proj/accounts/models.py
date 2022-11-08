from django.db import models
from django.contrib import auth


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        """Although we didn't assing value for username, it will still work, because it comes from auth.models.User"""
        return "@{}".format(self.username)