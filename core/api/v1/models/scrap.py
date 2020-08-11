from django.db import models


class ScrapModel(models.Model):
    name = models.CharField('Nome do(a) beneficiário(a)', max_length=255, null=True, blank=True)
    cpf = models.CharField('CPF do(a) beneficiário(a)', max_length=14, null=True, blank=True)
    birth = models.DateTimeField('Nascimento do(a) beneficiário(a)', null=True, blank=True)
    medical_records_number = models.CharField('Número do prontuário', null=True, max_length=30, blank=True)
    medical_records_date = models.DateTimeField('Data do prontuário', null=True, blank=True)
    professional_name = models.CharField('Nome do(a) profissional', max_length=255, null=True, blank=True)
    professional_code = models.CharField('Nome do(a) beneficiário', max_length=255, null=True, blank=True)
    url = models.URLField('Link prontuário', null=True, blank=True)

    date_created = models.DateTimeField('Criado em:', auto_now_add=True)
    last_update = models.DateTimeField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Index'
        verbose_name_plural = 'Indexes'

    def __str__(self):
        return self.name

    def get_full_name(self):
        return str(self)

    def date_published(self):
        return self.date_created.strftime('%B %d %Y')

    def get_short_name(self):
        return str(self).split(" ")[0]
