from django.db import models


class TasyPatient(models.Model):
    cd_empresa = models.PositiveIntegerField()
    ds_empresa = models.CharField(max_length=255)
    cd_estabelecimento = models.PositiveIntegerField()
    ds_estabelecimento = models.CharField(max_length=255)
    nr_atendimento = models.PositiveIntegerField(primary_key=True)
    nr_prontuario = models.PositiveIntegerField()
    cd_pessoa_fisica = models.CharField(max_length=255)
    ds_pessoa_fisica = models.CharField(max_length=255)
    nr_cpf = models.CharField(max_length=11)
    cd_convenio = models.PositiveIntegerField()
    ds_convenio = models.CharField(max_length=255)
    cd_setor_atendimento = models.PositiveIntegerField()
    ds_setor_atendimento = models.CharField(max_length=255)
    dt_entrada = models.DateTimeField()
    cd_unidade = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'amh_edok_atendimento_v'
