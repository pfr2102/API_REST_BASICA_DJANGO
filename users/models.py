from django.db import models

from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    email = models.EmailField(unique=True)
    group = models.ForeignKey(Group, related_name='custom_user_groups', on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []