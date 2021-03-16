from django.db import transaction

from rest_framework import viewsets, mixins

from core.api.v1.serializers.indexed_file import IndexedFileSerializer
from core.models import IndexedFileModel
from core.pagination import DefaultResultsSetPagination


class IndexedFileViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    queryset = IndexedFileModel.objects.all().order_by('-date_file')
    serializer_class = IndexedFileSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = []

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # stream = pdf_to_file() # Implementação movida para os jobs
        # response = StreamingHttpResponse(stream, content_type='application/json', status=200)

        return super(IndexedFileViewSet, self).create(request, args, kwargs)  # response
