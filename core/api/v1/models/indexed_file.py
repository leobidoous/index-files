from django.db import models


class Location(models.Model):
    location = models.CharField('Estabelecimento', max_length=255, unique=True)

    def __str__(self):
        return str(self.location)


class Sector(models.Model):
    sector_name = models.CharField('Setor', max_length=255)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name="sectors")

    def __str__(self):
        return str(self.sector_name)


class HealthInsurance(models.Model):
    health_insurance = models.CharField('Nome do convênio', max_length=255, unique=True)

    def __str__(self):
        return str(self.health_insurance)


class IndexedFileModel(models.Model):

    name = models.CharField('Nome do(a) beneficiário(a)', max_length=255, null=True, blank=True)
    filename = models.CharField('Nome do arquivo', max_length=255, unique=True)
    nr_cpf = models.CharField('CPF', max_length=20, null=True, blank=True)
    birth = models.DateTimeField('Nascimento do(a) beneficiário(a)', null=True, blank=True)
    medical_records_number = models.CharField('Número do prontuário', null=True, max_length=30, blank=True)
    date_in = models.DateTimeField('Data de entrada', null=True, blank=True)
    date_file = models.DateTimeField('Data do arquivo', null=True, blank=True)
    sex = models.CharField('Sexo', max_length=20, blank=True, null=True)
    health_insurance = models.ForeignKey(HealthInsurance, null=True, on_delete=models.DO_NOTHING, related_name='indexfiles')
    sector = models.CharField('Setor', max_length=255, null=True, blank=True)
    attendance_number = models.CharField('Número do atendimento', max_length=255, null=True, blank=True)
    uti = models.CharField('Número do leito', max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.DO_NOTHING, related_name='indexfiles')
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

    # def save(self, *args, **kwargs):
    #     if self.location:
    #         Location.objects.get_or_create(location=self.location)
    #     if self.health_insurance:
    #         HealthInsurance.objects.get_or_create(health_insurance=self.health_insurance)
    #
    #     super(IndexedFileModel, self).save(*args, **kwargs)
