from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError

from core.api.v1.forms.indexed_file import IndexedFilerForm
from core.models import IndexedFileModel, Location, HealthInsurance, Sector, Patient


class IndexedFilerAdmin(admin.ModelAdmin):
    form = IndexedFilerForm
    fields = ['name', 'nr_cpf', 'sex', 'birth', 'medical_records_number', 'date_in', 'health_insurance', 'location',
              'sector', 'tipo_documento', 'attendance_number', 'uti', 'url']

    def save_model(self, request, obj, form, change):
        try:
            super(IndexedFilerAdmin, self).save_model(request, obj, form, change)
        except ValidationError:
            messages.add_message(request, messages.ERROR, 'O usuário não foi salvo')
        # super(IndexedFilerAdmin, self).save_model(request, obj, form, change)


class LocationAdmin(admin.ModelAdmin):
    pass


class HealthInsuranceAdmin(admin.ModelAdmin):
    pass


class SectorAdmin(admin.ModelAdmin):
    pass

class PatientAdmin(admin.ModelAdmin):
    pass


admin.site.register(IndexedFileModel, IndexedFilerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(HealthInsurance, HealthInsuranceAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Patient, PatientAdmin)
