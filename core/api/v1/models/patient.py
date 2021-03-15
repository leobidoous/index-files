from django.db import models


class Patient(models.Model):
    cd_empresa = models.PositiveIntegerField(null=True, blank=True)
    ds_empresa = models.CharField(max_length=255, null=True, blank=True)
    cd_estabelecimento = models.PositiveIntegerField(null=True, blank=True)
    ds_estabelecimento = models.CharField(max_length=255, null=True, blank=True)
    nr_atendimento = models.PositiveIntegerField(null=True, blank=True)
    nr_prontuario = models.PositiveIntegerField(null=True, blank=True)
    cd_pessoa_fisica = models.CharField(max_length=255, null=True, blank=True)
    ds_pessoa_fisica = models.CharField(max_length=255, null=True, blank=True)
    nr_cpf = models.CharField(max_length=11, null=True, blank=True)
    cd_convenio = models.PositiveIntegerField(null=True, blank=True)
    ds_convenio = models.CharField(max_length=255, null=True, blank=True)
    cd_setor_atendimento = models.PositiveIntegerField(null=True, blank=True)
    ds_setor_atendimento = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

