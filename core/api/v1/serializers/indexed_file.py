from django.db import transaction
from rest_framework import serializers, mixins
from core.models import IndexedFileModel


class IndexedFileSerializer(serializers.ModelSerializer,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    class Meta:
        model = IndexedFileModel
        fields = '__all__'
        
    def create(self, validated_data):
        return super(IndexedFileSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(IndexedFileSerializer, self).update(instance, validated_data)

