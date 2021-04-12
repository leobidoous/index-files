import django_filters as filters

from core.models import Setor


class SetorFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Setor
        fields = ('nome',)
