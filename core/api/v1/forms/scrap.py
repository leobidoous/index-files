# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.api.v1.models.scrap import ScrapModel


class ScrapAdminCreationForm(UserCreationForm):
    class Meta:
        model = ScrapModel
        fields = ['name', 'cpf', 'birth', 'medical_records_number', 'medical_records_date', 'url']


class ScrapForm(forms.ModelForm):
    class Meta:
        model = ScrapModel
        fields = ['name', 'cpf', 'birth', 'medical_records_number', 'medical_records_date', 'url']

