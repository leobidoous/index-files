import os
import pathlib
import time
from pprint import pprint

from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter, HTMLConverter, PDFConverter, XMLConverter, PDFPageAggregator

from io import StringIO


def convert_pdf_to_txt():
    start_general = time.time()
    for path in pathlib.Path("files/AtePac_CT_6").iterdir():
        start = time.time()
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
        # print(path.name)

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

        print("---" * 8)
        print(text)

        print("name: {}".format(name))
        print("birth: {}".format(birth))
        print("sex: {}".format(sex))
        print("phone: {}".format(phone))
        print("sector: {}".format(sector))
        print("attendance: {}".format(attendance))
        print("medical_records_number: {}".format(medical_records_number))
        print("date_in: {}".format(date_in))
        print("health_insurance: {}".format(health_insurance))
        print("uti: {}".format(uti))

        converter.close()
        file_handle.close()

        end = time.time() - start
        print('Tempo parcial: {} seconds'.format(end))

    end = time.time() - start_general
    print('\nTempo geral: {} seconds'.format(end))


convert_pdf_to_txt()
