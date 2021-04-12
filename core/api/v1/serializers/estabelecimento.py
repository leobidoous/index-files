from rest_framework import serializers

from core.api.v1.serializers import SetorSerializer
from core.models import Estabelecimento


class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estabelecimento
        exclude = ('criado_em', 'atualizado_em')
