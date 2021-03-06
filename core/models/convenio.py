from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Convenio(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_('uuid'), default=uuid.uuid4, editable=False, unique=True)
    nome = models.CharField('Nome do convênio', max_length=255, unique=True)

    criado_em = models.DateTimeField('Criado em:', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em:', auto_now=True)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = 'convenio'
