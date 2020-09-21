# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.api.v1.models.indexed_file import IndexedFileModel


class IndexedFileAdminCreationForm(UserCreationForm):
    class Meta:
        model = IndexedFileModel
        fields = ['name', 'nr_cpf', 'sex', 'birth', 'medical_records_number', 'date_in', 'health_insurance', 'sector',
                  'attendance_number', 'uti', 'url']


class IndexedFilerForm(forms.ModelForm):
    class Meta:
        model = IndexedFileModel
        fields = ['name', 'nr_cpf', 'sex', 'birth', 'medical_records_number', 'date_in', 'health_insurance', 'sector',
                  'attendance_number', 'uti', 'url']
