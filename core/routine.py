

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.conf import settings


class RunJobs:

    def process_iop(self):
        # testes no iop

        import glob
        import os
        import shutil
        from qrcode.models import DocumentModel
        from core.api.v1.models.indexed_file import Location, HealthInsurance, IndexedFileModel, Sector
        from core.api.v1.models.tasy_patient import TasyPatient

        print("*********************** CARREGANDO IOP ********************************")
        path = settings.PATH_FILES+settings.PATH_IOP
        files_pdf = glob.glob(path + "*.pdf")

        for pdf_path in files_pdf:
            filter_name = os.path.split(pdf_path)[1]
            if DocumentModel.objects.filter(name__icontains=filter_name):
                print(f"Already exists on database the: {filter_name}")
                continue
            from qrcode.manage_qr_code import ManageQrCode

            qr_code = ManageQrCode(pdf_path)
            decoded_text = qr_code.get_decoded_text()

            print(decoded_text)

            try:
                shutil.move(path + filter_name, settings.PATH_MOVE_FILES_TO + "iop/" + filter_name)
            except FileNotFoundError:
                pass

            codes = decoded_text.split('-')
            nr_atendimento = codes[1]
            payload = {}
            payload['nr_atendimento'] = nr_atendimento

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
                    url='https://' + settings.SITE_NAME + settings.MEDIA_URL + "iop/" + filter_name
                )
                ###########################################################
            except TasyPatient.DoesNotExist:
                pass

            if decoded_text is not None:
                payload['name'] = filter_name
                payload['qr_code'] = decoded_text
                try:
                    payload['qr_code_image'] = qr_code.qr_code_image64.decode('utf-8')
                except:
                    pass
            else:
                payload['decoded_text'] = "Seu QR Code não foi identificado"

            print(payload)

    # def make_requests(self):
    #     print("carregando arquivos")
    #     requests.post(settings.URL_LOAD_FILES)


def start():
    _run_jobs = RunJobs()
    _now = datetime.now()
    scheduler = BackgroundScheduler()
    scheduler.add_job(_run_jobs.process_iop, 'interval', seconds=settings.TIME_TO_READ_FILES)
    scheduler.start()
