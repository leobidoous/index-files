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

from core.api.v1.serializers import ArquivoIndexadoRoutineSerializer
from core.models import Estabelecimento, Convenio, ArquivoIndexado, Setor, TasyPatient
from qrcode.manage_qr_code import ManageQrCode


def processar_digitalizado_iop():
    path = settings.PATH_FILES + settings.PATH_IOP
    files_pdf = glob.glob(path + "*.pdf")
    for pdf_path in files_pdf:
        filter_name = os.path.split(pdf_path)[1]

        qr_code = ManageQrCode(pdf_path)
        decoded_text = qr_code.get_decoded_text()

        try:
            shutil.copyfile(path + filter_name,
                            settings.PATH_MOVE_FILES_TO_LOCAL + settings.PATH_IOP + 'digitalizado/' + filter_name)

            shutil.move(path + filter_name,
                        settings.PATH_MOVE_FILES_TO + settings.PATH_IOP + 'digitalizado/' + filter_name)
        except FileNotFoundError:
            pass

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

            # Tenta encontrar um arquivo pré existente para efetuar um update nele (caso exista)
            arquivo = ArquivoIndexado.objects.filter(nome=paciente.ds_pessoa_fisica,
                                                     cpf=paciente.nr_cpf,
                                                     numero_atendimento=paciente.nr_atendimento,
                                                     numero_prontuario=paciente.nr_prontuario, )

            if arquivo:
                # Pega o último atualizado (por precaução)
                arquivo = arquivo.order_by('-atualizado_em').first()

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
                'url': settings.SITE_NAME + settings.MEDIA_URL + settings.PATH_IOP + 'digitalizado/' + filter_name,
                'tipo_documento': 'd',
            }

            try:
                if arquivo:
                    arquivo_anterior = arquivo.url.split(settings.MEDIA_URL)[1]
                    arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(instance=arquivo,
                                                                                   data=arquivo_indexado_dict,
                                                                                   partial=True)

                else:
                    arquivo_anterior = None
                    arquivo_indexado_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)

                arquivo_indexado_serializer.is_valid(raise_exception=True)
                arquivo_indexado_serializer.save()

                if arquivo_anterior:
                    os.remove(settings.PATH_MOVE_FILES_TO + arquivo_anterior)

            except Exception as e:
                print(repr(e))

        except TasyPatient.DoesNotExist:
            pass


def processar_prontuario_iop():
    for index, path in enumerate(pathlib.Path(settings.PATH_FILES + settings.PATH_PRONTUARIOS).iterdir()):
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
        try:
            shutil.copyfile(fh.name,
                            settings.PATH_MOVE_FILES_TO_LOCAL + caminho_base)

            shutil.move(fh.name, settings.PATH_MOVE_FILES_TO + caminho_base)
        except Exception as e:
            pass
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

                    os.remove(settings.PATH_MOVE_FILES_TO + arquivo_anterior)
                else:
                    arquivo_anterior = None
                    indexed_file_serializer = ArquivoIndexadoRoutineSerializer(data=arquivo_indexado_dict)
                indexed_file_serializer.is_valid(raise_exception=True)
                indexed_file_serializer.save()

                if arquivo_anterior:
                    os.remove(settings.PATH_MOVE_FILES_TO + arquivo_anterior)

            except Exception as e:
                repr(e)

        except Exception as e:
            repr(e)
            print("Impossível registrar o arquivo: " + path.name + ' || Estrutura inválida...')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(processar_digitalizado_iop,'interval',
                      seconds=settings.TIME_TO_READ_FILES,
                      id="processar_digitalizado_iop")
    scheduler.add_job(processar_prontuario_iop, 'interval',
                      seconds=settings.TIME_TO_READ_FILES,
                      id="processar_prontuario_iop")

    scheduler.start()
