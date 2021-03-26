from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
import django_filters
from core.api.v1.serializers import ArquivoIndexadoSerializer
from core.models import ArquivoIndexado, Estabelecimento, Convenio
from core.pagination import DefaultResultsSetPagination
from core.api.v1.filters import ArquivoIndexadoFilter


class ArquivoIndexadoViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin):
    serializer_class = ArquivoIndexadoSerializer
    filter_class = ArquivoIndexadoFilter
    pagination_class = DefaultResultsSetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Caso seja super usuário:
            # Recebe todos os estabelecimentos e todos os convênios
            estabelecimentos = list(Estabelecimento.objects.all().values_list('id', flat=True))
            convenios = list(Convenio.objects.all().values_list('id', flat=True))
        else:
            # Caso seja um usuário comum:
            # Recebe todos os estabelecimentos registrados e pode ver apenas os arquivos relacionados com seus convênios
            estabelecimentos = list(self.request.user.estabelecimentos.values_list('id', flat=True))
            convenios = list(self.request.user.convenios.values_list('id', flat=True))

        ordenado_por = self.request.query_params.get('ordenado_por')
        direcao_ordenacao = self.request.query_params.get('direcao_ordenacao')
        # fields = ArquivoIndexado._meta.get_fields()

        if ordenado_por and direcao_ordenacao and direcao_ordenacao in ['asc', 'desc']:
            order = '-' if direcao_ordenacao == 'desc' else ''
            order = order + ordenado_por
        else:
            order = 'nome'

        # Retorna a queryset filtrada por estabelecimentos e convênios
        return ArquivoIndexado.objects.select_related(
            'estabelecimento', 'convenio').filter(
            estabelecimento__id__in=estabelecimentos, convenio__id__in=convenios).order_by(order)

    def filter_queryset(self, queryset):
        return super(ArquivoIndexadoViewSet, self).filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        return super(ArquivoIndexadoViewSet, self).list(request, *args, **kwargs)

