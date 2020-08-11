import csv
import os
import pathlib
import time
from io import StringIO
from pprint import pprint

from django.http import StreamingHttpResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.v1.models.scrap import ScrapModel
from core.api.v1.serializers.scrap import ScrapSerializer
from core.pagination import DefaultResultsSetPagination

from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter


def scrap_pdf_file():
    start = time.time()
    for path in pathlib.Path("files").iterdir():
        laparams = LAParams()
        laparams.char_margin = 0.1
        laparams.word_margin = 0.1
        laparams.line_margin = 0.5
        laparams.boxes_flow = 0.5
        file_handle = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, file_handle, laparams=laparams)
        interpreter = PDFPageInterpreter(manager, converter)

        fh = open(str(path), 'rb')
        for page in PDFPage.get_pages(fh, maxpages=1):
            interpreter.process_page(page)
        fh.close()

        text = file_handle.getvalue()

        text = text.split("\n")
        text = text[10:]

        name = text[6]
        birth = text[7]
        sex = text[8]
        cpf = text[19]
        medical_records_date = text[10]
        medical_records_number = text[18]
        professional = text[45]
        professional_code = text[42]

        print("---" * 8)
        print("name: {}".format(name))
        print("birth: {}".format(birth))
        print("sex: {}".format(sex))
        print("cpf: {}".format(cpf))
        print("medical_records_date: {}".format(medical_records_date))
        print("medical_records_number: {}".format(medical_records_number))
        print("professional: {}".format(professional))
        print("professional_code: {}".format(professional_code))

        # close open handles
        converter.close()
        file_handle.close()

    end = time.time() - start
    print(end)


class ScrapViewSet(viewsets.ModelViewSet):
    queryset = ScrapModel.objects.all().order_by('-date_created')
    serializer_class = ScrapSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def get_files(self, request):
        response = StreamingHttpResponse(scrap_pdf_file())
        return response
