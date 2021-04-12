from django.db import transaction
from rest_framework import serializers, mixins
from rest_framework.exceptions import ValidationError

from core.api.v1.serializers.setor import SetorSerializer
from core.models import ArquivoIndexado


class ArquivoIndexadoSerializer(serializers.ModelSerializer,):
    setor = SetorSerializer()

    class Meta:
        model = ArquivoIndexado
        fields = '__all__'


class ArquivoIndexadoRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArquivoIndexado
        fields = '__all__'
