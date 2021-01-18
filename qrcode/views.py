import base64
import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Rest import
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONOpenAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser

# For managing qrcode
from .manage_qr_code import ManageQrCode

from  base64 import b64encode, b64decode
# Create your views here.


class QrCodeView(APIView):
    parser_class = (FileUploadParser,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'qrcode/detect_qr_code_extended.html'

    @staticmethod
    def get(request):
        return Response()

    @staticmethod
    def post(request):
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
            qr_code = ManageQrCode(myfile.file)
            decoded_text = qr_code.get_decoded_text()
            payload = {}
            if decoded_text is not None:
                payload['decoded_text'] = decoded_text
                payload['image'] = qr_code.qr_code_image64.decode('utf-8')
            else:
                payload['decoded_text'] = "Seu QR Code não foi identificado"

            return Response(payload, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class QrCodeAPI(APIView):
    """
        Recebe um PDF como bytes64 e conver
    """

    parser_classes = [MultiPartParser, FormParser, FileUploadParser]

    @staticmethod
    def post(request):
        print(request)
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            # Salvou em '/media/' o arquivo enviado por upload (com o nome .name e o arquivo myfile)
            myfile.name = myfile.name.replace(" ", "_")
            filename = fs.save(myfile.name, myfile)
            # Obtendo o link para o arquivo em /media/
            uploaded_file_url = fs.url(filename)
            # Retornando para a view
            print(fs.path(name=filename))
            print(fs.url(name=filename))
            qr_code = ManageQrCode(pdf_path=fs.path(name=filename))
            decoded_text = qr_code.get_decoded_text()
            payload = {'uploaded_file_url': uploaded_file_url}
            # print("Tempo total: " + "{:.2f}".format(qr_code.total_time))
            if decoded_text is not None:
                payload['decoded_text'] = decoded_text
                # with open(fs.path(name=filename).split('.pdf')[0] + '\\qr_code_detected.png', "rb") as image_file:
                #     image_data = base64.b64encode(image_file.read()).decode('utf-8')
                #     payload["image"] = image_data
            else:
                payload['decoded_text'] = "Seu QR Code não foi identificado"

            return Response(payload, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)
