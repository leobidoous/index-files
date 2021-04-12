from rest_framework import viewsets, mixins

from core.api.v1.filters import EstabelecimentoFilter
from core.api.v1.serializers import EstabelecimentoSerializer
from core.models import Estabelecimento
from core.pagination import DefaultResultsSetPagination


class EstabelecimentoViewSet(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin):
    serializer_class = EstabelecimentoSerializer
    queryset = Estabelecimento.objects.all()
    filter_class = EstabelecimentoFilter
    pagination_class = DefaultResultsSetPagination

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Estabelecimento.objects.prefetch_related('users').filter(users__id=self.request.user.id)
        return super(EstabelecimentoViewSet, self).get_queryset()

