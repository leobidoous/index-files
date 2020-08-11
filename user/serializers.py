from django.db import transaction
from rest_framework import serializers, mixins
from user.models import UserModel


class UserSerializer(serializers.ModelSerializer, mixins.CreateModelMixin):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password']
        action_fields = {
            "update": {
                "fields": ('email', 'username', 'password')
            },
            "partial_update": {
                "fields": ('email', 'username', 'password')
            }
        }
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user
