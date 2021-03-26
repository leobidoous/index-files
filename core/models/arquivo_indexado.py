import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.choices import ArquivoIndexadoChoices


class ArquivoIndexado(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_('uuid'), default=uuid.uuid4, editable=False, unique=True)
    nome = models.CharField('Nome do(a) beneficiário(a)', max_length=255, null=True, blank=True)
    nome_arquivo = models.CharField('Nome do arquivo', max_length=255, unique=True)
    cpf = models.CharField('CPF', max_length=20, null=True, blank=True)
    data_nascimento = models.DateTimeField('Nascimento do(a) beneficiário(a)', null=True, blank=True)
    numero_prontuario = models.CharField('Número do prontuário', null=True, max_length=30, blank=True)
    data_entrada = models.DateTimeField('Data de entrada', null=True, blank=True)
    data_arquivo = models.DateTimeField('Data do arquivo', null=True, blank=True)
    genero = models.CharField('Sexo', max_length=20, blank=True, null=True)
    convenio = models.ForeignKey('Convenio', null=True, on_delete=models.DO_NOTHING, related_name='indexfiles')
    setor = models.ForeignKey('Setor', on_delete=models.DO_NOTHING, related_name='indexfiles', null=True, blank=True)
    numero_atendimento = models.CharField('Número do atendimento', max_length=255, null=True, blank=True)
    uti = models.CharField('Número do leito', max_length=255, null=True, blank=True)
    estabelecimento = models.ForeignKey('Estabelecimento', null=True, on_delete=models.DO_NOTHING,
                                        related_name='arquivos_indexados')
    url = models.CharField('Link prontuário', max_length=200, null=True, blank=True)
    tipo_documento = models.CharField('Tipo do Documento', max_length=50, choices=ArquivoIndexadoChoices.tipo(),
                                      null=True, blank=True)

    criado_em = models.DateTimeField('Criado em:', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em:', auto_now=True)

    class Meta:
        verbose_name = 'Arquivo Indexado'
        verbose_name_plural = 'Arquivos Indexados'
        db_table = 'arquivo_indexado'

    def __str__(self):
        return str(self.nome)

    def get_full_name(self):
        return str(self)

    def date_published(self):
        return self.criado_em.strftime('%B %d %Y')

    def get_short_name(self):
        return str(self).split(" ")[0]

    def save(self, *args, **kwargs):
        super(ArquivoIndexado, self).save(*args, **kwargs)
