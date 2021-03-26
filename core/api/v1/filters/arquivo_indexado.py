from datetime import datetime, timedelta

import django_filters as filters

from core.models import ArquivoIndexado


class ArquivoIndexadoFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='icontains')
    data_entrada = filters.DateFilter(lookup_expr='contains')

    class Meta:
        model = ArquivoIndexado
        fields = ('nome', 'numero_prontuario', 'numero_atendimento',
                  'cpf', 'estabelecimento', 'data_entrada', 'setor', 'tipo_documento')
