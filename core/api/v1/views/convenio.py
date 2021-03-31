from rest_framework import viewsets, mixins

from core.api.v1.serializers import ConvenioSerializer
from core.models import Convenio
from core.pagination import DefaultResultsSetPagination


class ConvenioViewSet(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin):
    serializer_class = ConvenioSerializer
    queryset = Convenio.objects.all()
    pagination_class = DefaultResultsSetPagination
