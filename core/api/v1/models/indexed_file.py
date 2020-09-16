from django.db import models


class IndexedFileModel(models.Model):
    sexs = (('Masculino', 'Masculino'), ('Feminino', 'Feminino'))

    name = models.CharField('Nome do(a) beneficiário(a)', max_length=255, null=True, blank=True)
    filename = models.CharField('Nome do arquivo', max_length=255, unique=True)
    phone = models.CharField('Telefone do(a) beneficiário(a)', max_length=20, null=True, blank=True)
    birth = models.DateTimeField('Nascimento do(a) beneficiário(a)', null=True, blank=True)
    medical_records_number = models.CharField('Número do prontuário', null=True, max_length=30, blank=True)
    date_in = models.DateTimeField('Data de entrada', null=True, blank=True)
    sex = models.CharField('Sexo', max_length=10, choices=sexs, blank=True, null=True)
    health_insurance = models.CharField('Nome do convênio', max_length=255, null=True, blank=True)
    sector = models.CharField('Setor', max_length=255, null=True, blank=True)
    attendance_number = models.CharField('Número do atendimento', max_length=255, null=True, blank=True)
    uti = models.CharField('Número do leito', max_length=255, null=True, blank=True)
    url = models.CharField('Link prontuário', max_length=200, null=True, blank=True)

    date_created = models.DateTimeField('Criado em:', auto_now_add=True)
    last_update = models.DateTimeField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Index'
        verbose_name_plural = 'Indexes'

    def __str__(self):
        return str(self.name)

    def get_full_name(self):
        return str(self)

    def date_published(self):
        return self.date_created.strftime('%B %d %Y')

    def get_short_name(self):
        return str(self).split(" ")[0]
