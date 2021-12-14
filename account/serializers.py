from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
