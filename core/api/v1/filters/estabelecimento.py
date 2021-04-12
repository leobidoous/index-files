from datetime import datetime, timedelta

import django_filters as filters

from core.models import Estabelecimento


class EstabelecimentoFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Estabelecimento
        fields = ('nome',)
