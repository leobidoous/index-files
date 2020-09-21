import datetime
import os
import pathlib
import time
from datetime import date
from io import StringIO
from pprint import pprint

from django.db import transaction

from django.http import StreamingHttpResponse
from pdfminer.layout import LAParams
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.v1.models.indexed_file import IndexedFileModel
from core.api.v1.serializers.indexed_file import IndexedFileSerializer
from core.pagination import DefaultResultsSetPagination

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter

from django.conf import settings
import shutil


def pdf_to_file():
    for index, path in enumerate(pathlib.Path(settings.PATH_FILES).iterdir()):

        # start = time.time()

        file_handle = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, file_handle, laparams=LAParams(char_margin=0.01))
        interpreter = PDFPageInterpreter(manager, converter)

        fh = open(str(path), 'rb')
        for page in PDFPage.get_pages(fh, maxpages=1):
            interpreter.process_page(page)
        shutil.move(fh.name, settings.PATH_MOVE_FILES_TO+path.stem+'.pdf')
        fh.close()

        text = file_handle.getvalue()

        text = text.split('EVOLUÇÃO')[0].split('\n')

        indexed_file = dict({
            'filename': path.name,
            'name': text[7],
            'birth': datetime.datetime.strptime(text[8], '%d/%m/%Y'),
            'sex': text[9],
            'nr_cpf': text[10],
            'sector': text[32],
            'attendance_number': text[40],
            'medical_records_number': text[41],
            'date_in': datetime.datetime.strptime(text[30], '%d/%m/%Y %H:%M:%S'),
            'health_insurance': text[31],
            'uti': text[33],
            'location': text[43],
            'url': 'https://'+settings.SITE_NAME+settings.MEDIA_URL+path.stem+'.pdf'
        })

        try:
            indexed_file_serializer = IndexedFileSerializer(data=indexed_file)
            indexed_file_serializer.is_valid(raise_exception=True)
            indexed_file = indexed_file_serializer.save()
        except Exception as e:
            print(e)
            pass

        converter.close()
        file_handle.close()

        # end = time.time() - start
        # print('Tempo parcial: {} seconds'.format(end))

        yield Response(indexed_file)


class IndexedFileViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    queryset = IndexedFileModel.objects.all().order_by('-medical_records_number')
    serializer_class = IndexedFileSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = []

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        stream = pdf_to_file()
        response = StreamingHttpResponse(stream, content_type='application/json', status=200)

        return response
