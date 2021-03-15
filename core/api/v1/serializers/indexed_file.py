from django.db import transaction
from rest_framework import serializers, mixins
from core.models import IndexedFileModel


class IndexedFileSerializer(serializers.ModelSerializer, mixins.CreateModelMixin):
    class Meta:
        model = IndexedFileModel
        exclude = ('id', 'date_created', 'last_update')

    @transaction.atomic
    def create(self, validated_data):
        return super(IndexedFileSerializer, self).create(validated_data)
