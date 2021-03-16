import glob
import os

from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

# For managing qrcode
from core.models import IndexedFileModel, Location, HealthInsurance
from .manage_qr_code import ManageQrCode
from .models import DocumentModel
from .serializers import QrCodeSerializer
from core.models.tasy_patient import TasyPatient


class QrCodeView(APIView):
    parser_class = (FileUploadParser,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'qrcode/detect_qr_code.html'

    @staticmethod
    def get(request):
        return Response()

    @staticmethod
    def insert_pdf_in_db():
        # Caminho para o pdf
        path = ("C:\\Users\\Rafael\\Documents\\PDF_QRCODE\\enviados\\")
        files_pdf = glob.glob(path + "*.pdf")

        for pdf_path in files_pdf:
            filter_name = os.path.split(pdf_path)[1]
            if DocumentModel.objects.filter(name__icontains=filter_name):
                print(f"Already exists on database the: {filter_name}")
                continue
            qr_code = ManageQrCode(pdf_path)
            decoded_text = qr_code.get_decoded_text()
            payload = {}
            if decoded_text is not None:
                payload['name'] = filter_name
                payload['qr_code'] = decoded_text
                try:
                    payload['qr_code_image'] = qr_code.qr_code_image64.decode('utf-8')
                except:
                    pass
                serializer = QrCodeSerializer(data=payload)
                if serializer.is_valid():
                    serializer.save()
            else:
                payload['decoded_text'] = "Seu QR Code não foi identificado"
        return Response()

    @staticmethod
    def post(request):
        try:
            myfile = request.FILES['myfile']
            qr_code = ManageQrCode(myfile.file)
            decoded_text = qr_code.get_decoded_text()
            payload = {}
            documents = DocumentModel.objects.filter(name__icontains=myfile.name)

            if documents:
                for model in documents:
                    payload['name'] = myfile.name
                    payload['qr_code'] = model.qr_code
                    payload['qr_code_image'] = model.qr_code_image
                    codes = decoded_text.split('-')
                    nr_atendimento = codes[1]
                    payload['nr_atendimento'] = nr_atendimento

                    try:
                        patient = TasyPatient.objects.using('tasy_erp').get(nr_atendimento=int(nr_atendimento))
                        payload['patient'] = patient

                        ######### Inserindo dados do paciente aqui #################
                        location, created = Location.objects.get_or_create(location=patient.ds_estabelecimento)

                        health_insurance, created = HealthInsurance.objects.get_or_create(health_insurance=patient.ds_convenio)

                        IndexedFileModel.objects.get_or_create(
                            name=patient.ds_pessoa_fisica,
                            filename=myfile.name,
                            nr_cpf=patient.nr_cpf,
                            medical_records_number=patient.nr_prontuario,
                            health_insurance=health_insurance,
                            sector=patient.ds_setor_atendimento,
                            attendance_number=patient.nr_atendimento,
                            location=location,
                            date_in=patient.dt_entrada,
                            uti=patient.cd_unidade
                        )
                        ###########################################################
                    except TasyPatient.DoesNotExist:
                        pass
                    break
                return Response(payload, status=status.HTTP_200_OK)

            if decoded_text is not None:
                payload['name'] = myfile.name
                payload['qr_code'] = decoded_text
                if qr_code.qr_code_image64 is not None:
                    payload['qr_code_image'] = qr_code.qr_code_image64.decode('utf-8')
                else:
                    payload['qr_code_image'] = None
                serializer = QrCodeSerializer(data=payload)

                if DocumentModel.objects.filter(name__icontains=myfile.name):
                    return Response(payload, status=status.HTTP_200_OK)

                if serializer.is_valid():
                    serializer.save()

                codes = decoded_text.split('-')
                nr_atendimento = codes[1]
                payload['nr_atendimento'] = nr_atendimento
            else:
                payload['decoded_text'] = "Seu QR Code não foi identificado"
            return Response(payload, status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
