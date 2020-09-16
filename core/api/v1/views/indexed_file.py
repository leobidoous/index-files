import datetime
import os
import pathlib
import time
from datetime import date
from io import StringIO
from pprint import pprint

from django.db import transaction

from django.http import StreamingHttpResponse
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
        converter = TextConverter(manager, file_handle)
        interpreter = PDFPageInterpreter(manager, converter)

        fh = open(str(path), 'rb')
        for page in PDFPage.get_pages(fh, maxpages=1):
            interpreter.process_page(page)
        shutil.move(fh.name, settings.PATH_MOVE_FILES_TO+path.stem)
        fh.close()

        text = file_handle.getvalue()

        text = text.split("Sinais")[0]
        text = text.split("Evolução")[0]

        indexed_file = dict({
            'filename': path.name,
            'name': text.split("Paciente")[1].split('Atendimento')[0],
            'birth': datetime.datetime.strptime(text.split("Data Nasc.")[1][:10], '%d/%m/%Y'),
            'sex': text.split("Sexo")[1].split('Dt. Entrada')[0],
            'phone': text.split("Telefone")[1].split('Convênio')[0],
            'sector': text.split("Setor")[1].split("Leito")[0],
            'attendance_number': text.split("Atendimento")[2].split('Data Nasc.')[0],
            'medical_records_number': text.split('Prontuário')[1].split('Sexo')[0],
            'date_in': datetime.datetime.strptime(text.split("Dt. Entrada")[1][:19], '%d/%m/%Y %H:%M:%S'),
            'health_insurance': text.split("Convênio")[1].split('Setor')[0],
            'uti': 'Leito{}'.format(text.split("Leito")[1]),
            'url': 'https://www.'+settings.SITE_NAME+settings.MEDIA_URL+path.stem
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
    queryset = IndexedFileModel.objects.all().order_by('-date_created')
    serializer_class = IndexedFileSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = []

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        stream = pdf_to_file()
        response = StreamingHttpResponse(stream, content_type='application/json', status=200)
        return response
