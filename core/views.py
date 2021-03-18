import datetime

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from core.models import IndexedFileModel, Location, Sector, HealthInsurance


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
        "tipo_documento": ""
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
            if self.request.GET.get('locations') is None:
                selected_location = 0
                context['loc_filter'] = 0
            else:
                selected_location = int(self.request.GET.get('locations'))
                context['loc_filter'] = self.request.GET.get('locations')

            if self.request.GET.get('sectors') is None:
                selected_sector = 0
                context['sec_filter'] = 0
            else:
                selected_sector = int(self.request.GET.get('sectors'))
                context['sec_filter'] = self.request.GET.get('sectors')

            if self.request.GET.get('name') is None:
                context['name_filter'] = ''
            else:
                context['name_filter'] = self.request.GET.get('name')

            if self.request.GET.get('cpf') is None:
                context['cpf_filter'] = ''
            else:
                context['cpf_filter'] = self.request.GET.get('cpf')

            if self.request.GET.get('medical_records_number') is None:
                context['mr_filter'] = ''
            else:
                context['mr_filter'] = self.request.GET.get('medical_records_number')

            if self.request.GET.get('attendance_number') is None:
                context['at_filter'] = ''
            else:
                context['at_filter'] = self.request.GET.get('attendance_number')

            if self.request.GET.get('date_in') is None:
                context['dt_filter'] = ''
            else:
                context['dt_filter'] = self.request.GET.get('date_in')

            if self.request.GET.get('tipo_documento') is None:
                context['tipo_filter'] = ''
            else:
                context['tipo_filter'] = self.request.GET.get('tipo_documento')

            new_location = selected_location

            # Tenta encontrar uma location com o id selecionado
            if self.request.user.is_superuser:
                loc_temp = Location.objects.all().filter(id=selected_location)
            else:
                loc_temp = self.request.user.locations.all().filter(id=selected_location)

            # Se não foi possível encontrar a localização e o setor foi selecionado,
            # então vamos encontrar a location desse setor
            if not loc_temp and selected_sector != 0:
                # Se entrar aqui, então não tem prioridade de exibição (ou seja, Todos(location = 0) é o escolhido
                if self.request.user.is_superuser:
                    loc_temp = Location.objects.filter(sectors__id=selected_sector)
                else:
                    loc_temp = self.request.user.locations.filter(sectors__id=selected_sector)

                # Atribui uma nova id para a selecionada (para definir a prioridade do contexto)
                if loc_temp:
                    new_location = loc_temp.get().id
                else:
                    selected_location = 0
                    selected_sector = 0

            if loc_temp:
                context['locations'].append(loc_temp.get())
                sec_temp = loc_temp.get().sectors.filter(pk=selected_sector)
                if sec_temp:
                    context['sectors'].append(sec_temp.get())

                for sector in loc_temp.get().sectors.all():
                    if sector.pk != selected_sector:
                        context['sectors'].append(sector)
            else:
                context['all'] = True

            # Preenche as outras locations, sem ser a selecionada.
            if self.request.user.is_superuser:
                locations = Location.objects.exclude(id=new_location)
            else:
                locations = self.request.user.locations.exclude(id=new_location)

            for loc in locations:
                context['locations'].append(loc)
                # Caso o setor seja 0 e a location seja 0,
                # então iremos imprimir todos os setores disponíveis, de todas as localizações
                if selected_location == 0:
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
        self.filters['tipo_documento'] = self.request.GET.get('tipo_documento')

        if not user.is_anonymous:
            if user.is_superuser:
                # qs = IndexedFileModel.objects.all().order_by("-date_file")
                locations_user = Location.objects.all()
                health_insurance_user = HealthInsurance.objects.all()
            else:
                locations_user = user.locations.all()
                health_insurance_user = user.health_insurances.all()

            lc_nr = self.request.GET.get('locations')
            locations = []

            if lc_nr is None or int(lc_nr) == 0:
                for obj in locations_user:
                    locations.append(obj.pk)
            else:
                if lc_nr is not None and Location.objects.filter(id=int(lc_nr)):
                    locations.append(int(lc_nr))
                else:
                    for obj in locations_user:
                        locations.append(obj.pk)

            sector_nr = self.request.GET.get('sectors')
            if sector_nr is not None:
                if locations_user.filter(id__in=locations, sectors__id=sector_nr):
                    sector_nr = int(sector_nr)
                else:
                    sector_nr = 0
            else:
                sector_nr = 0

            health_insurance = []
            for obj in health_insurance_user:
                health_insurance.append(obj.pk)
            if sector_nr == 0:
                qs = IndexedFileModel.objects.filter(location__id__in=locations).all().order_by("-date_file")
            else:
                sector = locations_user.filter(id__in=locations).filter(sectors__id=sector_nr).first().sectors.filter(id=sector_nr).get()
                qs = IndexedFileModel.objects.filter(location__id__in=locations,
                                                     sector=sector.pk).all().order_by("-date_file")
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
            if self.filters['tipo_documento']:
                qs = qs.filter(tipo_documento__iexact=self.filters['tipo_documento'])

            return qs.filter(health_insurance_id__in=health_insurance).order_by('name')
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
