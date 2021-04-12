from django.db import transaction

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core.api.v1.filters import SetorFilter
from core.api.v1.serializers import SetorSerializer
from core.models import Setor
from core.pagination import DefaultResultsSetPagination


class SetorViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    serializer_class = SetorSerializer
    filter_class = SetorFilter
    permission_classes = (IsAuthenticated, )
    pagination_class = DefaultResultsSetPagination

    def get_queryset(self):
        # Verifica se é super usuário para definir o acesso à todos os setores a partir daquele estabelecimento
        if self.request.user.is_superuser:
            return Setor.objects.filter(
                estabelecimento_id=self.kwargs.get('estabelecimento_pk')
            ).order_by('nome')
        # Caso seja um usuário comum, ele recebe apenas os setores cujo faz parte dos usuários
        return Setor.objects.select_related(
            'estabelecimento'
        ).prefetch_related(
            'estabelecimento__users'
        ).filter(
            estabelecimento_id=self.kwargs.get('estabelecimento_pk'),
            estabelecimento__users__id=self.request.user.id
        ).order_by('nome')
