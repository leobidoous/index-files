from rest_framework import serializers

from core.models import Convenio


class ConvenioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Convenio
        fields = '__all__'
