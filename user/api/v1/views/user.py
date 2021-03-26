from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core.pagination import DefaultResultsSetPagination
from user.api.v1.serializers import UserSerializer, UserEstabelecimentoConvenioSerializer
from user.models import UserModel


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserModel.objects.all().order_by('-criado_em')
    serializer_class = UserSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = [IsAuthenticated]


class UserEstabelecimentoViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.UpdateModelMixin):
    queryset = UserModel.objects.all().order_by('-criado_em')
    serializer_class = UserEstabelecimentoConvenioSerializer
    permission_classes = [IsAuthenticated, ]


class UserConvenioViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin):
    queryset = UserModel.objects.all().order_by('-criado_em')
    serializer_class = UserEstabelecimentoConvenioSerializer
    permission_classes = [IsAuthenticated, ]
