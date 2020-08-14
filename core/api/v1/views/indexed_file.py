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


def pdf_to_file():
    start_general = time.time()
    for index, path in enumerate(pathlib.Path("files/AtePac_CT_6").iterdir()):
        start = time.time()
        total_files = len(os.listdir("files/AtePac_CT_6"))
        file_handle = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, file_handle)
        interpreter = PDFPageInterpreter(manager, converter)

        fh = open(str(path), 'rb')
        for page in PDFPage.get_pages(fh, maxpages=1):
            interpreter.process_page(page)
        fh.close()

        text = file_handle.getvalue()

        text = text.split("Sinais")[0]
        text = text.split("Evolução")[0]

        name = text.split("Paciente")[1].split('Atendimento')[0]
        birth = text.split("Data Nasc.")[1][:10]
        sex = text.split("Sexo")[1].split('Dt. Entrada')[0]
        phone = text.split("Telefone")[1].split('Convênio')[0]
        sector = text.split("Setor")[1].split("Leito")[0]
        attendance = text.split("Atendimento")[2].split('Data Nasc.')[0]
        medical_records_number = text.split('Prontuário')[1].split('Sexo')[0]
        date_in = text.split("Dt. Entrada")[1][:19]
        health_insurance = text.split("Convênio")[1].split('Setor')[0]
        uti = 'Leito{}'.format(text.split("Leito")[1])

        converter.close()
        file_handle.close()

        end = time.time() - start
        print('Tempo parcial: {} seconds'.format(end))

        d = dict({
            'name': name,
            'birth': birth,
            'sex': sex,
            'phone': phone,
            'sector': sector,
            'attendance': attendance,
            'medical_records_number': medical_records_number,
            'date_in': date_in,
            'health_insurance': health_insurance,
            'uti': uti
        })

        yield Response('{}/{} - {}\n'.format(index + 1, total_files, d))
        if index == 2:
            break

    end = time.time() - start_general
    print('\nTempo geral: {} seconds'.format(end))


class IndexedFileViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    queryset = IndexedFileModel.objects.all().order_by('-date_created')
    serializer_class = IndexedFileSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        def aaa():
            for index, path in enumerate(pathlib.Path("files/AtePac_CT_6").iterdir()):
                start = time.time()
                total_files = len(os.listdir("files/AtePac_CT_6"))
                file_handle = StringIO()
                manager = PDFResourceManager()
                converter = TextConverter(manager, file_handle)
                interpreter = PDFPageInterpreter(manager, converter)

                fh = open(str(path), 'rb')
                for page in PDFPage.get_pages(fh, maxpages=1):
                    interpreter.process_page(page)
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
                    'attendance': text.split("Atendimento")[2].split('Data Nasc.')[0],
                    'medical_records_number': text.split('Prontuário')[1].split('Sexo')[0],
                    'date_in': datetime.datetime.strptime(text.split("Dt. Entrada")[1][:19], '%d/%m/%Y %H:%M:%S'),
                    'health_insurance': text.split("Convênio")[1].split('Setor')[0],
                    'uti': 'Leito{}'.format(text.split("Leito")[1])
                })

                pprint(indexed_file)

                indexed_file_serializer = IndexedFileSerializer(data=indexed_file)
                indexed_file_serializer.is_valid(raise_exception=True)
                indexed_file = indexed_file_serializer.save()

                converter.close()
                file_handle.close()

                end = time.time() - start
                print('Tempo parcial: {} seconds'.format(end))

                yield indexed_file
                # if index == 1:
                #     break

        stream = aaa()
        response = StreamingHttpResponse(stream, content_type='application/json', status=200)
        return response
        return super(IndexedFileViewSet, self).create(response)
