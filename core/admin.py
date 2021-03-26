from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError

from core.api.v1.forms import ArquivoIndexadoForm
from core.models import Estabelecimento, Setor, ArquivoIndexado, Paciente, Convenio


class ArquivoIndexadoAdmin(admin.ModelAdmin):
    form = ArquivoIndexadoForm
    fields = ['nome', 'cpf', 'genero', 'data_nascimento', 'numero_prontuario', 'data_entrada', 'convenio', 'setor',
              'numero_atendimento', 'uti', 'url', 'tipo_documento']

    def save_model(self, request, obj, form, change):
        try:
            super(ArquivoIndexadoAdmin, self).save_model(request, obj, form, change)
        except ValidationError:
            messages.add_message(request, messages.ERROR, 'O usuário não foi salvo')
        # super(IndexedFilerAdmin, self).save_model(request, obj, form, change)


class EstabelecimentoAdmin(admin.ModelAdmin):
    pass


class ConvenioAdmin(admin.ModelAdmin):
    pass


class SetorAdmin(admin.ModelAdmin):
    pass


class PacienteAdmin(admin.ModelAdmin):
    pass


admin.site.register(ArquivoIndexado, ArquivoIndexadoAdmin)
admin.site.register(Estabelecimento, EstabelecimentoAdmin)
admin.site.register(Convenio, ConvenioAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Paciente, PacienteAdmin)
