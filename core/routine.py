import datetime
import glob
import os
import pathlib
import shutil
from datetime import datetime
from io import StringIO

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from rest_framework.response import Response

from core.api.v1.serializers.indexed_file import IndexedFileSerializer
from core.models import Location, HealthInsurance, IndexedFileModel, Sector
from core.models import TasyPatient
from qrcode.models import DocumentModel

from qrcode.manage_qr_code import ManageQrCode


def processar_digitalizado_iop():
    # testes no iop

    print("*********************** CARREGANDO IOP ********************************")
    path = settings.PATH_FILES+settings.PATH_IOP
    files_pdf = glob.glob(path + "*.pdf")

    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]
        # Verifica se o pdf já está na base DocumentModel
        # Se já existir então já foi lido e ignora o resto da iteração
        if DocumentModel.objects.filter(name__iexact=filter_name):
            print(f"Already exists on database the: {filter_name}")
            continue

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        print(decoded_text)

        try:
            shutil.move(path + filter_name, settings.PATH_MOVE_FILES_TO + "iop/" + filter_name)
        except FileNotFoundError:
            pass

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            patient = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['patient'] = patient

            ######### Inserindo dados do paciente aqui #################
            location, created = Location.objects.get_or_create(location=patient.ds_estabelecimento)

            health_insurance, created = HealthInsurance.objects.get_or_create(health_insurance=patient.ds_convenio)

            # Apenas criando os setores, porém não está sendo relacionado ao paciente,
            # pois nao modelagem antiga não existia vínculo relacional,
            # então para nõo impactar nos arquivos já salvos, até pensarmos em um solução
            # o vínculo continua não relacional

            Sector.objects.get_or_create(sector_name=patient.ds_setor_atendimento,
                                         location=location)

            IndexedFileModel.objects.get_or_create(
                name=patient.ds_pessoa_fisica,
                filename=filter_name,
                nr_cpf=patient.nr_cpf,
                medical_records_number=patient.nr_prontuario,
                health_insurance=health_insurance,
                sector=patient.ds_setor_atendimento,
                attendance_number=patient.nr_atendimento,
                location=location,
                date_in=patient.dt_entrada,
                uti=patient.cd_unidade,
                birth=patient.dt_nascimento,
                sex=patient.ie_sexo,
                url='https://' + settings.SITE_NAME + settings.MEDIA_URL + "iop/" + filter_name,
                tipo_documento='d',
            )
            ###########################################################
        except TasyPatient.DoesNotExist:
            pass

        if decoded_text is not None:
            payload['name'] = filter_name
            payload['qr_code'] = decoded_text
            try:
                payload['qr_code_image'] = qr_code.qr_code_image64.decode('utf-8')
            except Exception:
                pass
        else:
            payload['decoded_text'] = "Seu QR Code não foi identificado"

        print(payload)


def processar_prontuario_iop():
    print("carregando arquivos")
    for index, path in enumerate(pathlib.Path(settings.PATH_FILES).iterdir()):

        # start = time.time()

        file_handle = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, file_handle, laparams=LAParams(char_margin=0.01))
        interpreter = PDFPageInterpreter(manager, converter)

        fh = open(str(path), 'rb')
        for page in PDFPage.get_pages(fh, maxpages=1):
            interpreter.process_page(page)
        shutil.move(fh.name, settings.PATH_MOVE_FILES_TO + path.stem + '.pdf')
        fh.close()

        text = file_handle.getvalue()

        text = text.split('Profissional')[0].split('\n')

        try:
            indexed_file_dict = {
                'filename': path.name,
                'name': text[55],
                'birth': datetime.datetime.strptime(text[56], '%d/%m/%Y'),
                'sex': text[57],
                'nr_cpf': text[58],
                'sector': text[18],
                'medical_records_number': text[27],
                'date_in': datetime.datetime.strptime(text[16], '%d/%m/%Y %H:%M:%S'),
                'date_file': datetime.datetime.strptime(text[60], '%d/%m/%Y'),
                'uti': text[19],
                'url': 'https://' + settings.SITE_NAME + settings.MEDIA_URL + path.stem + '.pdf'
            }

            if text[26]:
                indexed_file_dict['attendance_number'] = str(text[26])
                if type(indexed_file_dict['attendance_number']) == type(tuple()):
                    indexed_file_dict['attendance_number'] = indexed_file_dict['attendance_number'][0]
            if text[29]:
                location, created = Location.objects.get_or_create(location=text[29])
                indexed_file_dict['location'] = location.pk
            if text[17]:
                health_insurance, created = HealthInsurance.objects.get_or_create(health_insurance=text[17])
                indexed_file_dict['health_insurance'] = health_insurance.pk

            try:
                indexed_file_dict['tipo_documento'] = 'p'
                indexed_file_serializer = IndexedFileSerializer(data=indexed_file_dict)
                indexed_file_serializer.is_valid(raise_exception=True)
                indexed_file_serializer.save()
            except Exception as e:
                print(e)
                pass

            converter.close()
            file_handle.close()

            # end = time.time() - start
            # print('Tempo parcial: {} seconds'.format(end))

            yield Response(indexed_file_dict)
        except Exception as e:
            print(e)
            print('Impossível registrar o arquivo: ' + path.name + ' || Estrutura inválida...')
            pass
            # yield Response('Impossível registrar o arquivo: ' + path.name + ' || Estrutura inválida...')

    requests.post(settings.URL_LOAD_FILES)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(processar_digitalizado_iop, 'interval',
                      seconds=settings.TIME_TO_READ_FILES,
                      id="processar_digitalizado_iop")
    scheduler.add_job(processar_prontuario_iop, 'interval',
                      seconds=settings.TIME_TO_READ_FILES,
                      id="processar_prontuario_iop")

    scheduler.start()
