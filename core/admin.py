from django.contrib import admin

from core.api.v1.forms.indexed_file import IndexedFilerForm
from core.models import IndexedFileModel, Location, HealthInsurance


class IndexedFilerAdmin(admin.ModelAdmin):
    form = IndexedFilerForm
    fields = ['name', 'nr_cpf', 'sex', 'birth', 'medical_records_number', 'date_in', 'health_insurance', 'location',
              'sector',
              'attendance_number', 'uti', 'url']


class LocationAdmin(admin.ModelAdmin):
    pass


class HealthInsuranceAdmin(admin.ModelAdmin):
    pass


admin.site.register(IndexedFileModel, IndexedFilerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(HealthInsurance, HealthInsuranceAdmin)
