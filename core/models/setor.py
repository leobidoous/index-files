from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Setor(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_('uuid'), default=uuid.uuid4, editable=False, unique=True)
    nome = models.CharField('Setor', max_length=255, unique=True)
    estabelecimento = models.ForeignKey('Estabelecimento', on_delete=models.DO_NOTHING, related_name="setores", null=True)

    criado_em = models.DateTimeField('Criado em:', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em:', auto_now=True)

    def __str__(self):
        return str(self.nome)

    class Meta:
        unique_together=['nome', 'estabelecimento']
        db_table = 'setor'
