# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.models import ArquivoIndexado


class ArquivoIndexadoCreateForm(UserCreationForm):
    class Meta:
        model = ArquivoIndexado
        fields = ['nome', 'cpf', 'genero', 'data_nascimento', 'numero_prontuario', 'data_entrada', 'convenio', 'setor',
                  'numero_atendimento', 'uti', 'url', 'tipo_documento']


class ArquivoIndexadoForm(forms.ModelForm):
    class Meta:
        model = ArquivoIndexado
        fields = ['nome', 'cpf', 'genero', 'data_nascimento', 'numero_prontuario', 'data_entrada', 'convenio', 'setor',
                  'numero_atendimento', 'uti', 'url', 'tipo_documento']
