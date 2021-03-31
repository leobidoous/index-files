from datetime import datetime, timedelta

import django_filters as filters

from core.models import ArquivoIndexado


class ArquivoIndexadoFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='icontains')
    data_entrada = filters.DateTimeFilter(method='filter_data')

    class Meta:
        model = ArquivoIndexado
        fields = ('nome', 'numero_prontuario', 'numero_atendimento',
                  'cpf', 'estabelecimento', 'data_entrada', 'setor', 'tipo_documento')

    @staticmethod
    def filter_data(self, queryset, name, value):
        return queryset.filter(data_entrada__range=[value, value + timedelta(days=1)])
