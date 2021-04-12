from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import status
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler


class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/index.html'
    permission_classes = []

    def get(self, request):
        payload = jwt_payload_handler(self.request.user)
        token = jwt_encode_handler(payload)

        host = settings.SITE_NAME + '/api/v1'
        return Response(status=status.HTTP_200_OK, data={'host': host, 'token': token})


class AdministradorView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/administracao.html'
    permission_classes = []

    def get(self, request):
        payload = jwt_payload_handler(self.request.user)
        token = jwt_encode_handler(payload)

        host = settings.SITE_NAME + '/api/v1'
        return Response(status=status.HTTP_200_OK, data={'host': host, 'token': token})


class SolicitarRedefinirSenha(PasswordResetView):
    template_name = 'registration/solicitar-redefinir-senha.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('core:password_reset_done')


class RedefinirSenhaCompleto(TemplateView):
    template_name = 'registration/redefinir-senha-completo.html'
    success_url = reverse_lazy('core:password_reset_confirm')


class RedefinirSenha(PasswordResetConfirmView):
    template_name = 'registration/redefinir-senha.html'
    success_url = reverse_lazy('core:login')
