import datetime
import re

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from core.api.v1.models.scrap import ScrapModel


# Create your views here.
class HomeView(ListView, LoginRequiredMixin):
    model = ScrapModel
    paginate_by = 10
    context_object_name = 'files'
    template_name = 'core/index.html'

    filters = {
        "name": "",
        "cpf": "",
        "birth": "",
        "medical_records_number": "",
        "medical_records_date": "",
        "professional_name": "",
        "professional_code": "",
    }

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(object_list=None, **kwargs)
        context['filters'] = self.filters
        return context

    def get_queryset(self, *args, **kwargs):
        self.filters['name'] = self.request.GET.get('name')
        self.filters['cpf'] = self.request.GET.get('cpf')
        self.filters['birth'] = self.request.GET.get('birth')
        self.filters['medical_records_number'] = self.request.GET.get('medical_records_number')
        self.filters['medical_records_date'] = self.request.GET.get('medical_records_date')
        self.filters['professional_name'] = self.request.GET.get('professional_name')
        self.filters['professional_code'] = self.request.GET.get('professional_code')

        qs = ScrapModel.objects.all().order_by("-date_created")

        if self.filters['name']:
            qs = qs.filter(name__contains=self.filters['name'])
        if self.filters['cpf']:
            cpf = re.sub("[^0-9]", "", self.filters['cpf'])
            qs = qs.filter(cpf=cpf)
        if self.filters['birth']:
            date = datetime.datetime.strptime(self.filters['birth'], '%Y-%m-%d')
            qs = qs.filter(birth__day=date.day, birth__month=date.month, birth__year=date.year)
        if self.filters['medical_records_number']:
            qs = qs.filter(medical_records_number=self.filters['medical_records_number'])
        if self.filters['medical_records_date']:
            date = datetime.datetime.strptime(self.filters['medical_records_date'], '%Y-%m-%d')
            qs = qs.filter(medical_records_date__day=date.day, medical_records_date__month=date.month,
                           medical_records_date__year=date.year)
        if self.filters['professional_name']:
            qs = qs.filter(professional_name__contains=self.filters['professional_name'])
        if self.filters['professional_code']:
            qs = qs.filter(professional_code=self.filters['professional_code'])

        return qs


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
