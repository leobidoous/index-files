from django.contrib.auth.models import User, Group
from qrcode.models import DocumentModel
from rest_framework import serializers


class QrCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentModel
        fields = ['name', 'qr_code', 'qr_code_image']
