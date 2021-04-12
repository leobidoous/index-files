from django.db import transaction
from rest_framework import mixins
from rest_framework import serializers

from core.api.v1.serializers import EstabelecimentoSerializer
from core.api.v1.serializers.convenio import ConvenioSerializer
from user.models import UserModel


class UserSerializer(serializers.ModelSerializer, mixins.CreateModelMixin):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password', 'criado_em', 'atualizado_em']
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


class UserEstabelecimentoConvenioSerializer(serializers.ModelSerializer):
    estabelecimentos = EstabelecimentoSerializer(many=True, required=False)
    convenios = ConvenioSerializer(many=True, required=False)

    class Meta:
        model = UserModel
        fields = ('id', 'estabelecimentos', 'convenios')