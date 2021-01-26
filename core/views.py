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
        if not self.request.user.is_anonymous:
            context['locations'] = []
            context['sectors'] = []
            selected_location = 0
            selected_sector = 0

            if self.request.GET.get('locations'):
                selected_location = self.request.GET.get('locations')
                loc_temp = self.request.user.locations.all().filter(id=int(selected_location))
                if loc_temp:
                    context['locations'].append(loc_temp.get())
                    selected_sector = self.request.GET.get('sectors')
                    sec_temp = loc_temp.get().sectors.filter(pk=int(selected_sector))
                    if sec_temp:
                        context['sectors'].append(sec_temp.get())

                    for sector in loc_temp.get().sectors.all():
                        if sector.pk != int(selected_sector):
                            context['sectors'].append(sector)
                            
            for loc in self.request.user.locations.exclude(id=int(selected_location)):
                if loc.id != selected_location:
                    context['locations'].append(loc)
                    if int(selected_sector) == 0 and int(selected_location) == 0:
                        for sector in loc.sectors.all():
                            context['sectors'].append(sector)
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
                qs = IndexedFileModel.objects.all().order_by("-date_file")
            else:
                locations_user = user.locations.all()
                sectors_user = user.locations.all()
                health_insurance_user = user.health_insurances.all()

                lc_nr = self.request.GET.get('locations')
                locations = []
                if lc_nr is None or int(lc_nr) == 0:
                    for obj in locations_user:
                        locations.append(obj.pk)
                else:
                    locations.append(int(lc_nr))

                sector_nr = self.request.GET.get('sectors')
                if sector_nr is not None:
                    sector_nr = int(sector_nr)
                sectors = []
                sectors = locations_user.first().sectors.all()
                '''
                if lc_nr is None or int(sector_nr) == 0:
                    for obj in sectors_user:
                        sectors.append(obj.pk)
                else:
                    locations.append(int(lc_nr))
                '''

                health_insurance = []
                for obj in health_insurance_user:
                    health_insurance.append(obj.pk)
                if sector_nr is None or sector_nr == 0:
                    qs = IndexedFileModel.objects.filter(location__id__in=locations).all().order_by("-date_file")
                else:
                    sector_name = locations_user.filter(id=int(lc_nr)).first().sectors.filter(id=sector_nr).get().sector_name
                    qs = IndexedFileModel.objects.filter(location__id__in=locations,
                                                         sector__iexact=sector_name).all().order_by("-date_file")


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
