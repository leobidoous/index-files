import datetime
import re

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from core.api.v1.models.indexed_file import IndexedFileModel


# Create your views here.
class HomeView(ListView, LoginRequiredMixin):
    model = IndexedFileModel
    paginate_by = 10
    context_object_name = 'files'
    template_name = 'core/index.html'

    filters = {
        "sex": "",
        "uti": "",
        "name": "",
        "birth": "",
        "sector": "",
        "date_in": "",
        "health_insurance": "",
        "attendance_number": "",
        "medical_records_number": "",
    }

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(object_list=None, **kwargs)
        context['filters'] = self.filters
        url = 'https://intcare.edok.com.br/api/DocView.php?'
        url += 'k=' + settings.EDOK_API_KEY
        context['url'] = url
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        self.filters['name'] = self.request.GET.get('name')
        self.filters['nr_cpf'] = self.request.GET.get('cpf')
        self.filters['birth'] = self.request.GET.get('birth')
        self.filters['sector'] = self.request.GET.get('sector')
        self.filters['date_in'] = self.request.GET.get('date_in')
        self.filters['health_insurance'] = self.request.GET.get('health_insurance')
        self.filters['attendance_number'] = self.request.GET.get('attendance_number')
        self.filters['medical_records_number'] = self.request.GET.get('medical_records_number')

        if not user.is_anonymous:
            if user.is_superuser:
                qs = IndexedFileModel.objects.all().order_by("-date_created")
            else:
                locations_user = user.locations.all()
                health_insurance_user = user.health_insurances.all()
    
                locations = []
                for obj in locations_user:
                    locations.append(obj.pk)
                health_insurance = []
                for obj in health_insurance_user:
                    health_insurance.append(obj.pk)

                qs = IndexedFileModel.objects.filter(location__id__in=locations).filter(
                    health_insurance__id__in=health_insurance).all().order_by("-date_created")
    
            if self.filters['name']:
                qs = qs.filter(name__contains=self.filters['name'])
            if self.filters['birth']:
                date = datetime.datetime.strptime(self.filters['birth'], '%Y-%m-%d')
                qs = qs.filter(birth__day=date.day, birth__month=date.month, birth__year=date.year)
            if self.filters['medical_records_number']:
                qs = qs.filter(medical_records_number=self.filters['medical_records_number'])
            if self.filters['date_in']:
                date = datetime.datetime.strptime(self.filters['date_in'], '%Y-%m-%d')
                qs = qs.filter(date_in__day=date.day, date_in__month=date.month, date_in__year=date.year)
            if self.filters['sector']:
                qs = qs.filter(sector__icontains=self.filters['sector'])
            if self.filters['nr_cpf']:
                qs = qs.filter(nr_cpf__iexact=self.filters['nr_cpf'].replace('.', '').replace('-', ''))
            if self.filters['attendance_number']:
                qs = qs.filter(attendance_number__icontains=self.filters['attendance_number'])
    
            return qs
        return super(HomeView, self).get_queryset()


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
