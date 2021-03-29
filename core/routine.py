import datetime
import glob
import os
import pathlib
import shutil
from datetime import datetime
from io import StringIO

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from core.api.v1.serializers.indexed_file import IndexedFileSerializer
from core.models import Location, HealthInsurance, IndexedFileModel, Sector
from core.models import TasyPatient
from qrcode.manage_qr_code import ManageQrCode


def processar_digitalizado_iop():
    directory = settings.PATH_IOP
    path = settings.PATH_FILES + directory

    files_pdf = glob.glob(path + "*.pdf")

    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        caminho_base = directory + 'digitalizado/' + filter_name


        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            patient = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['patient'] = patient

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, location e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            location, created = Location.objects.get_or_create(location=patient.ds_estabelecimento)
            sector, created = Sector.objects.get_or_create(sector_name=patient.ds_setor_atendimento, location=location)
            health_insurance, created = HealthInsurance.objects.get_or_create(health_insurance=patient.ds_convenio)

            # Tenta encontrar um arquivo pré existente para efetuar um update nele (caso exista)
            indexed = IndexedFileModel.objects.filter(name=patient.ds_pessoa_fisica,
                                                      nr_cpf=patient.nr_cpf,
                                                      attendance_number=patient.nr_atendimento,
                                                      medical_records_number=patient.nr_prontuario,)

            if indexed:
                # Pega o último atualizado (por precaução)
                indexed = indexed.order_by('-updated_at').first()

            # Payload do IndexFile
            indexed_file_dict = {
                'name': patient.ds_pessoa_fisica,
                'filename': filter_name,
                'nr_cpf': patient.nr_cpf,
                'medical_records_number': patient.nr_prontuario,
                'health_insurance': health_insurance.pk,
                'sector': sector.pk,
                'attendance_number': patient.nr_atendimento,
                'location': location.pk,
                'date_in': patient.dt_entrada,
                'date_file': datetime.now(),
                'uti': patient.cd_unidade,
                'birth': patient.dt_nascimento,
                'sex': patient.ie_sexo,
                'url': 'https://' + settings.SITE_NAME + settings.MEDIA_URL + directory + 'digitalizado/' + filter_name,
                'tipo_documento': 'd',
            }
            try:
                if indexed:
                    last_file = indexed.url.split(settings.SITE_NAME + settings.MEDIA_URL)[1]
                    indexed_file_serializer = IndexedFileSerializer(instance=indexed,
                                                                    data=indexed_file_dict,
                                                                    partial=True)
                    os.remove(settings.PATH_MOVE_FILES_TO + last_file)
                else:
                    indexed_file_serializer = IndexedFileSerializer(data=indexed_file_dict)

                indexed_file_serializer.is_valid(raise_exception=True)
                indexed_file_serializer.save()
            except Exception as e:
                print(repr(e))

            '''
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
                url='https://' + settings.SITE_NAME + settings.MEDIA_URL + "ftp-iop/" + filter_name,
                tipo_documento='d',
            )
            '''

            try:
                # shutil.copyfile(path + filter_name,
                #                 settings.PATH_MOVE_FILES_TO_LOCAL + caminho_base)

                shutil.move(path + filter_name,
                            settings.PATH_MOVE_FILES_TO + caminho_base)
            except FileNotFoundError:
                pass
        except TasyPatient.DoesNotExist:
            pass


def processar_digitalizado_domed():
    # O diretório precisa ser definido aqui

    directory = settings.PATH_DOMED
    path = settings.PATH_FILES + directory

    files_pdf = glob.glob(path + "*.pdf")

    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        caminho_base = directory + 'digitalizado/' + filter_name


        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            patient = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['patient'] = patient

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, location e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            location, created = Location.objects.get_or_create(location=patient.ds_estabelecimento)
            sector, created = Sector.objects.get_or_create(sector_name=patient.ds_setor_atendimento, location=location)
            health_insurance, created = HealthInsurance.objects.get_or_create(health_insurance=patient.ds_convenio)

            # Tenta encontrar um arquivo pré existente para efetuar um update nele (caso exista)
            indexed = IndexedFileModel.objects.filter(name=patient.ds_pessoa_fisica,
                                                      nr_cpf=patient.nr_cpf,
                                                      attendance_number=patient.nr_atendimento,
                                                      medical_records_number=patient.nr_prontuario,)

            if indexed:
                # Pega o último atualizado (por precaução)
                indexed = indexed.order_by('-updated_at').first()

            # Payload do IndexFile
            indexed_file_dict = {
                'name': patient.ds_pessoa_fisica,
                'filename': filter_name,
                'nr_cpf': patient.nr_cpf,
                'medical_records_number': patient.nr_prontuario,
                'health_insurance': health_insurance.pk,
                'sector': sector.pk,
                'attendance_number': patient.nr_atendimento,
                'location': location.pk,
                'date_in': patient.dt_entrada,
                'date_file': datetime.now(),
                'uti': patient.cd_unidade,
                'birth': patient.dt_nascimento,
                'sex': patient.ie_sexo,
                'url': 'https://' + settings.SITE_NAME + settings.MEDIA_URL + directory + 'digitalizado/' + filter_name,
                'tipo_documento': 'd',
            }
            try:
                if indexed:
                    last_file = indexed.url.split(settings.SITE_NAME + settings.MEDIA_URL)[1]
                    indexed_file_serializer = IndexedFileSerializer(instance=indexed,
                                                                    data=indexed_file_dict,
                                                                    partial=True)
                    os.remove(settings.PATH_MOVE_FILES_TO + last_file)
                else:
                    indexed_file_serializer = IndexedFileSerializer(data=indexed_file_dict)

                indexed_file_serializer.is_valid(raise_exception=True)
                indexed_file_serializer.save()
            except Exception as e:
                print(repr(e))

            '''
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
                url='https://' + settings.SITE_NAME + settings.MEDIA_URL + "ftp-iop/" + filter_name,
                tipo_documento='d',
            )
            '''

            try:
                # shutil.copyfile(path + filter_name,
                #                 settings.PATH_MOVE_FILES_TO_LOCAL + caminho_base)

                shutil.move(path + filter_name,
                            settings.PATH_MOVE_FILES_TO + caminho_base)
            except FileNotFoundError:
                pass
        except TasyPatient.DoesNotExist:
            pass

def processar_prontuarios():
    # prontuários sem qrcode de todas as unidades são processados aqui

    for index, path in enumerate(pathlib.Path(settings.PATH_PRONTUARIOS).iterdir()):
        # start = time.time()
        file_handle = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, file_handle, laparams=LAParams(char_margin=0.01))
        interpreter = PDFPageInterpreter(manager, converter)
        fh = open(str(path), 'rb')
        for page in PDFPage.get_pages(fh, maxpages=1):
            interpreter.process_page(page)
        fh.close()

        text = file_handle.getvalue()
        caminho_base = settings.PATH_IOP + 'prontuario/' + path.stem + '.pdf'

        text = text.split('Profissional')[0].split('\n')

        try:
            # por enquanto não será necessário
            # shutil.copyfile(fh.name,
            #                 settings.PATH_MOVE_FILES_TO_LOCAL + caminho_base)

            shutil.move(fh.name, settings.PATH_MOVE_FILES_TO + caminho_base)
        except Exception as e:
            pass

        try:
            indexed_file_dict = {
                'filename': path.name,
                'name': text[55],
                'birth': datetime.strptime(text[56], '%d/%m/%Y'),
                'sex': text[57],
                'nr_cpf': text[58],
                'sector': text[18],
                'medical_records_number': text[27],
                'date_in': datetime.strptime(text[16], '%d/%m/%Y %H:%M:%S'),
                'date_file': datetime.strptime(text[60], '%d/%m/%Y'),
                'uti': text[19],
                'url': 'https://' + settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'p',
            }

            # Filtra o attendance_number abaixo
            indexed = IndexedFileModel.objects.filter(name=text[55],
                                                      nr_cpf=text[58],
                                                      medical_records_number=text[27], )

            if text[26]:
                indexed_file_dict['attendance_number'] = str(text[26])
                if type(indexed_file_dict['attendance_number']) == type(tuple()):
                    indexed_file_dict['attendance_number'] = indexed_file_dict['attendance_number'][0]
                # Filtra por attendance_number
                if indexed:
                    indexed = indexed.filter(attendance_number=indexed_file_dict['attendance_number'])

            if text[29]:
                location, created = Location.objects.get_or_create(location=text[29])
                indexed_file_dict['location'] = location.pk
                if text[18]:
                    sector, created = Sector.objects.get_or_create(location=location, sector_name=text[18])
                    indexed_file_dict['sector'] = sector.pk

            if text[17]:
                health_insurance, created = HealthInsurance.objects.get_or_create(health_insurance=text[17])
                indexed_file_dict['health_insurance'] = health_insurance.pk

            try:
                if indexed:
                    # Se existir uma query, então pega o último e atualiza
                    indexed = indexed.order_by('-updated_at').first()
                    arquivo_anterior = indexed.url.split(settings.SITE_NAME + settings.MEDIA_URL)[1]
                    indexed_file_serializer = IndexedFileSerializer(instance=indexed, data=indexed_file_dict, partial=True)

                    os.remove(settings.PATH_MOVE_FILES_TO + arquivo_anterior)

                else:
                    arquivo_anterior = None
                    indexed_file_serializer = IndexedFileSerializer(data=indexed_file_dict)
                indexed_file_serializer.is_valid(raise_exception=True)
                indexed_file_serializer.save()

                if arquivo_anterior:
                    os.remove(settings.PATH_MOVE_FILES_TO + arquivo_anterior)

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
            print("Impossível registrar o arquivo: " + path.name + ' || Estrutura inválida...')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(processar_digitalizado_iop, 'interval', seconds=settings.TIME_TO_READ_FILES,)
    scheduler.add_job(processar_digitalizado_domed, 'interval', seconds=settings.TIME_TO_READ_FILES,)
    scheduler.add_job(processar_prontuarios, 'interval', seconds=settings.TIME_TO_READ_FILES, )

    scheduler.start()
