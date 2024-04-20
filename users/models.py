from django.db import models

from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    email = models.EmailField(unique=True)
    group = models.ForeignKey(Group, related_name='custom_user_groups', on_delete=models.SET_NULL, null=True)

    #comenta estas lineas cuando creas un superusuario en la terminal
    """ USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] """