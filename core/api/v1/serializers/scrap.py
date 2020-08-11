from django.db import transaction
from rest_framework import serializers, mixins
from core.api.v1.models.scrap import ScrapModel


class ScrapSerializer(serializers.ModelSerializer, mixins.CreateModelMixin):
    class Meta:
        model = ScrapModel
        exclude = ('id', 'date_created', 'last_update')

    @transaction.atomic
    def create(self, validated_data):
        return super(ScrapSerializer, self).create(validated_data)
