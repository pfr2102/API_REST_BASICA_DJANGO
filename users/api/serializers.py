from rest_framework import serializers
from django.contrib.auth.models import Group

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 
                  'last_name', 'password', 'is_active', 'is_staff','group']
        
# Serializadores para Group osea grupos de permisos como roles
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']        