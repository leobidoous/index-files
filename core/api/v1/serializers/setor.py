from rest_framework import serializers, mixins

from core.models import Setor


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        exclude = ('criado_em', 'atualizado_em')

