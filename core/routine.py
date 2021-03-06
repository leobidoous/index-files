import datetime
import glob
import os
import pathlib
import shutil
from datetime import datetime
from io import StringIO

from PyPDF2 import PdfFileReader
from apscheduler.schedulers.background import BackgroundScheduler
from celery import shared_task
from django.conf import settings
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from core.api.v1.serializers import ArquivoIndexadoRoutineSerializer
from core.models import Estabelecimento, Convenio, ArquivoIndexado, Setor, TasyPatient
from qrcode.manage_qr_code import ManageQrCode


@shared_task
def processar_digitalizado_iop():
    pasta = settings.PATH_IOP
    path = settings.PATH_FILES + pasta
    files_pdf = glob.glob(path + "*.pdf")
    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            paciente = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['paciente'] = paciente

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, estabelecimento e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            estabelecimento, created = Estabelecimento.objects.get_or_create(nome=paciente.ds_estabelecimento)
            setor, created = Setor.objects.get_or_create(nome=paciente.ds_setor_atendimento,
                                                         estabelecimento_id=estabelecimento.id)
            convenio, created = Convenio.objects.get_or_create(nome=paciente.ds_convenio)

            caminho_base = pasta + 'digitalizado/' + filter_name

            # Payload do IndexFile
            arquivo_indexado_dict = {
                'nome': paciente.ds_pessoa_fisica,
                'nome_arquivo': filter_name,
                'cpf': paciente.nr_cpf,
                'numero_prontuario': paciente.nr_prontuario,
                'convenio': convenio.id,
                'setor': setor.id,
                'numero_atendimento': paciente.nr_atendimento,
                'estabelecimento': estabelecimento.id,
                'data_entrada': paciente.dt_entrada,
                'data_arquivo': datetime.now(),
                'uti': paciente.cd_unidade,
                'data_nascimento': paciente.dt_nascimento,
                'genero': paciente.ie_sexo,
                # http para debug e https para o servidor
                'url': settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'd',
            }

            try:
                arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)

                arquivo_indexado_serializer.is_valid(raise_exception=True)
                arquivo_indexado_serializer.save()

                try:
                    shutil.move(path + filter_name,
                                settings.PATH_MOVE_FILES_TO + caminho_base)
                except FileNotFoundError:
                    pass

            except Exception as e:
                print(repr(e))

        except TasyPatient.DoesNotExist:
            pass


@shared_task
def processar_digitalizado_domed():
    pasta = settings.PATH_DOMED
    path = settings.PATH_FILES + pasta
    files_pdf = glob.glob(path + "*.pdf")
    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            paciente = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['paciente'] = paciente

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, estabelecimento e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            estabelecimento, created = Estabelecimento.objects.get_or_create(nome=paciente.ds_estabelecimento)
            setor, created = Setor.objects.get_or_create(nome=paciente.ds_setor_atendimento,
                                                         estabelecimento_id=estabelecimento.id)
            convenio, created = Convenio.objects.get_or_create(nome=paciente.ds_convenio)

            caminho_base = pasta + 'digitalizado/' + filter_name

            # Payload do IndexFile
            arquivo_indexado_dict = {
                'nome': paciente.ds_pessoa_fisica,
                'nome_arquivo': filter_name,
                'cpf': paciente.nr_cpf,
                'numero_prontuario': paciente.nr_prontuario,
                'convenio': convenio.id,
                'setor': setor.id,
                'numero_atendimento': paciente.nr_atendimento,
                'estabelecimento': estabelecimento.id,
                'data_entrada': paciente.dt_entrada,
                'data_arquivo': datetime.now(),
                'uti': paciente.cd_unidade,
                'data_nascimento': paciente.dt_nascimento,
                'genero': paciente.ie_sexo,
                # http para debug e https para o servidor
                'url': settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'd',
            }

            try:
                arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)
                arquivo_indexado_serializer.is_valid(raise_exception=True)
                arquivo_indexado_serializer.save()

                try:
                    shutil.move(path + filter_name,
                                settings.PATH_MOVE_FILES_TO + caminho_base)
                except FileNotFoundError:
                    pass

            except Exception as e:
                print(repr(e))

        except TasyPatient.DoesNotExist:
            pass


@shared_task
def processar_digitalizado_hoc():
    pasta = settings.PATH_HOC
    path = settings.PATH_FILES + pasta
    files_pdf = glob.glob(path + "*.pdf")
    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            paciente = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['paciente'] = paciente

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, estabelecimento e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            estabelecimento, created = Estabelecimento.objects.get_or_create(nome=paciente.ds_estabelecimento)
            setor, created = Setor.objects.get_or_create(nome=paciente.ds_setor_atendimento,
                                                         estabelecimento_id=estabelecimento.id)
            convenio, created = Convenio.objects.get_or_create(nome=paciente.ds_convenio)

            caminho_base = pasta + 'digitalizado/' + filter_name

            # Payload do IndexFile
            arquivo_indexado_dict = {
                'nome': paciente.ds_pessoa_fisica,
                'nome_arquivo': filter_name,
                'cpf': paciente.nr_cpf,
                'numero_prontuario': paciente.nr_prontuario,
                'convenio': convenio.id,
                'setor': setor.id,
                'numero_atendimento': paciente.nr_atendimento,
                'estabelecimento': estabelecimento.id,
                'data_entrada': paciente.dt_entrada,
                'data_arquivo': datetime.now(),
                'uti': paciente.cd_unidade,
                'data_nascimento': paciente.dt_nascimento,
                'genero': paciente.ie_sexo,
                # http para debug e https para o servidor
                'url': settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'd',
            }

            try:
                arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)

                arquivo_indexado_serializer.is_valid(raise_exception=True)
                arquivo_indexado_serializer.save()

                try:
                    shutil.move(path + filter_name,
                                settings.PATH_MOVE_FILES_TO + caminho_base)
                except FileNotFoundError:
                    pass

            except Exception as e:
                print(repr(e))

        except TasyPatient.DoesNotExist:
            pass


@shared_task
def processar_digitalizado_barreiras():
    pasta = settings.PATH_BARREIRAS
    path = settings.PATH_FILES + pasta
    files_pdf = glob.glob(path + "*.pdf")
    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            paciente = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['paciente'] = paciente

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, estabelecimento e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            estabelecimento, created = Estabelecimento.objects.get_or_create(nome=paciente.ds_estabelecimento)
            setor, created = Setor.objects.get_or_create(nome=paciente.ds_setor_atendimento,
                                                         estabelecimento_id=estabelecimento.id)
            convenio, created = Convenio.objects.get_or_create(nome=paciente.ds_convenio)

            caminho_base = pasta + 'digitalizado/' + filter_name

            # Payload do IndexFile
            arquivo_indexado_dict = {
                'nome': paciente.ds_pessoa_fisica,
                'nome_arquivo': filter_name,
                'cpf': paciente.nr_cpf,
                'numero_prontuario': paciente.nr_prontuario,
                'convenio': convenio.id,
                'setor': setor.id,
                'numero_atendimento': paciente.nr_atendimento,
                'estabelecimento': estabelecimento.id,
                'data_entrada': paciente.dt_entrada,
                'data_arquivo': datetime.now(),
                'uti': paciente.cd_unidade,
                'data_nascimento': paciente.dt_nascimento,
                'genero': paciente.ie_sexo,
                # http para debug e https para o servidor
                'url': settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'd',
            }

            try:
                arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)

                arquivo_indexado_serializer.is_valid(raise_exception=True)
                arquivo_indexado_serializer.save()

                try:
                    shutil.move(path + filter_name,
                                settings.PATH_MOVE_FILES_TO + caminho_base)
                except FileNotFoundError:
                    pass

            except Exception as e:
                print(repr(e))

        except TasyPatient.DoesNotExist:
            pass


@shared_task
def processar_digitalizado_paraupebas():
    pasta = settings.PATH_PARAUPEBAS
    path = settings.PATH_FILES + pasta
    files_pdf = glob.glob(path + "*.pdf")
    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            paciente = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['paciente'] = paciente

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, estabelecimento e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            estabelecimento, created = Estabelecimento.objects.get_or_create(nome=paciente.ds_estabelecimento)
            setor, created = Setor.objects.get_or_create(nome=paciente.ds_setor_atendimento,
                                                         estabelecimento_id=estabelecimento.id)
            convenio, created = Convenio.objects.get_or_create(nome=paciente.ds_convenio)

            caminho_base = pasta + 'digitalizado/' + filter_name

            # Payload do IndexFile
            arquivo_indexado_dict = {
                'nome': paciente.ds_pessoa_fisica,
                'nome_arquivo': filter_name,
                'cpf': paciente.nr_cpf,
                'numero_prontuario': paciente.nr_prontuario,
                'convenio': convenio.id,
                'setor': setor.id,
                'numero_atendimento': paciente.nr_atendimento,
                'estabelecimento': estabelecimento.id,
                'data_entrada': paciente.dt_entrada,
                'data_arquivo': datetime.now(),
                'uti': paciente.cd_unidade,
                'data_nascimento': paciente.dt_nascimento,
                'genero': paciente.ie_sexo,
                # http para debug e https para o servidor
                'url': settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'd',
            }

            try:
                arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)

                arquivo_indexado_serializer.is_valid(raise_exception=True)
                arquivo_indexado_serializer.save()

                try:
                    shutil.move(path + filter_name,
                                settings.PATH_MOVE_FILES_TO + caminho_base)
                except FileNotFoundError:
                    pass

            except Exception as e:
                print(repr(e))

        except TasyPatient.DoesNotExist:
            pass


@shared_task
def processar_digitalizado_ituiutaba():
    pasta = settings.PATH_ITUIUTABA
    path = settings.PATH_FILES + pasta
    files_pdf = glob.glob(path + "*.pdf")
    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        if decoded_text is None:
            # Ignora o resto da iteração caso o QR Code não tenha sido identificado ou não exista
            continue
        print(decoded_text)

        codes = decoded_text.split('-')
        nr_atendimento = codes[1]
        payload = {'nr_atendimento': nr_atendimento}

        try:
            paciente = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
            payload['paciente'] = paciente

            ######### Inserindo dados do paciente aqui #################

            # Cria um setor, estabelecimento e health insurance.
            # Baseado no nome do setor de atendimento ou obtém um se já existir com esse nome
            estabelecimento, created = Estabelecimento.objects.get_or_create(nome=paciente.ds_estabelecimento)
            setor, created = Setor.objects.get_or_create(nome=paciente.ds_setor_atendimento,
                                                         estabelecimento_id=estabelecimento.id)
            convenio, created = Convenio.objects.get_or_create(nome=paciente.ds_convenio)

            caminho_base = pasta + 'digitalizado/' + filter_name

            # Payload do IndexFile
            arquivo_indexado_dict = {
                'nome': paciente.ds_pessoa_fisica,
                'nome_arquivo': filter_name,
                'cpf': paciente.nr_cpf,
                'numero_prontuario': paciente.nr_prontuario,
                'convenio': convenio.id,
                'setor': setor.id,
                'numero_atendimento': paciente.nr_atendimento,
                'estabelecimento': estabelecimento.id,
                'data_entrada': paciente.dt_entrada,
                'data_arquivo': datetime.now(),
                'uti': paciente.cd_unidade,
                'data_nascimento': paciente.dt_nascimento,
                'genero': paciente.ie_sexo,
                # http para debug e https para o servidor
                'url': settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'd',
            }

            try:
                arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)

                arquivo_indexado_serializer.is_valid(raise_exception=True)
                arquivo_indexado_serializer.save()

                try:
                    shutil.move(path + filter_name,
                                settings.PATH_MOVE_FILES_TO + caminho_base)
                except FileNotFoundError:
                    pass

            except Exception as e:
                print(repr(e))

        except TasyPatient.DoesNotExist:
            pass


@shared_task
def processar_prontuarios():
    for index, path in enumerate(pathlib.Path(settings.PATH_PRONTUARIOS).iterdir()):
        # start = time.time()
        file_handle = StringIO()

        manager = PDFResourceManager()
        converter = TextConverter(manager, file_handle, laparams=LAParams(char_margin=0.01))
        interpreter = PDFPageInterpreter(manager, converter)
        fh = open(str(path), 'rb')
        file = PdfFileReader(str(path))
        if file.isEncrypted:
            print("Arquivo " + path.name + " está encriptado!!")
            fh.close()
            try:
                shutil.move(fh.name,
                            settings.PATH_MOVE_FILES_TO +
                            settings.PATH_PRONTUARIOS_ERRO +
                            settings.PATH_PRONTUARIOS_ERRO_ENCRIPTADO +
                            path.stem + '.pdf')

            except Exception as e:
                pass
            continue
        for page in PDFPage.get_pages(fh, maxpages=1, check_extractable=False):
            interpreter.process_page(page)
        fh.close()

        text = file_handle.getvalue()
        caminho_base = 'prontuarios/' + path.stem + '.pdf'

        text = text.split('Profissional')[0].split('\n')
        try:

            arquivo_indexado_dict = {
                'nome_arquivo': path.name,
                'nome': text[55],
                'data_nascimento': datetime.strptime(text[56], '%d/%m/%Y'),
                'genero': text[57],
                'cpf': text[58],
                'setor': text[18],
                'numero_prontuario': text[27],
                'data_entrada': datetime.strptime(text[16], '%d/%m/%Y %H:%M:%S'),
                'data_arquivo': datetime.strptime(text[60], '%d/%m/%Y'),
                'uti': text[19],
                'url': settings.SITE_NAME + settings.MEDIA_URL + caminho_base,
                'tipo_documento': 'p',
            }

            # Filtra o numero_atendimento abaixo
            arquivo = ArquivoIndexado.objects.filter(nome=text[55],
                                                     cpf=text[58],
                                                     numero_prontuario=text[27], )

            if text[26]:
                arquivo_indexado_dict['numero_atendimento'] = str(text[26])
                if type(arquivo_indexado_dict['numero_atendimento']) == type(tuple()):
                    arquivo_indexado_dict['numero_atendimento'] = arquivo_indexado_dict['numero_atendimento'][0]
                # Filtra por numero_atendimento
                if arquivo:
                    arquivo.filter(numero_atendimento=arquivo_indexado_dict['numero_atendimento'])

            if text[29]:
                estabelecimento, created = Estabelecimento.objects.get_or_create(nome=text[29])
                arquivo_indexado_dict['estabelecimento'] = estabelecimento.id
                if text[18]:
                    setor, created = Setor.objects.get_or_create(nome=text[18], estabelecimento_id=estabelecimento.id)
                    arquivo_indexado_dict['setor'] = setor.id

            if text[17]:
                convenio, created = Convenio.objects.get_or_create(nome=text[17])
                arquivo_indexado_dict['convenio'] = convenio.id

            try:
                if arquivo:
                    arquivo = arquivo.order_by('-atualizado_em').first()
                    arquivo_anterior = arquivo.url.split(settings.SITE_NAME + settings.MEDIA_URL)[1]
                    # Se existir uma query, então pega o último e atualiza
                    indexed_file_serializer = ArquivoIndexadoRoutineSerializer(instance=arquivo,
                                                                               data=arquivo_indexado_dict,
                                                                               partial=True)
                    try:
                        os.remove(settings.PATH_MOVE_FILES_TO + arquivo_anterior)
                    except Exception as e:
                        pass
                else:
                    indexed_file_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)
                indexed_file_serializer.is_valid(raise_exception=True)
                indexed_file_serializer.save()
                try:
                    # shutil.copyfile(fh.name,
                    #                 settings.PATH_MOVE_FILES_TO_LOCAL + caminho_base)

                    shutil.move(fh.name, settings.PATH_MOVE_FILES_TO + caminho_base)

                except Exception as e:
                    pass

            except Exception as e:
                repr(e)

        except Exception as e:
            repr(e)
            try:
                shutil.move(fh.name,
                            settings.PATH_MOVE_FILES_TO +
                            settings.PATH_PRONTUARIOS_ERRO +
                            settings.PATH_PRONTUARIOS_ERRO_ESTRUTURAL +
                            path.stem + '.pdf')
            except Exception as e:
                pass
            print("Impossível registrar o arquivo: " + path.name + ' || Estrutura inválida...')

# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(processar_digitalizado_iop, 'interval',
#                       seconds=settings.TIME_TO_READ_FILES,
#                       id="processar_digitalizado_iop")
#     scheduler.add_job(processar_digitalizado_domed, 'interval',
#                       seconds=settings.TIME_TO_READ_FILES,
#                       id="processar_digitalizado_domed")
#     scheduler.add_job(processar_prontuarios, 'interval',
#                       seconds=settings.TIME_TO_READ_FILES,
#                       id="processar_prontuarios")
#
#     scheduler.start()
