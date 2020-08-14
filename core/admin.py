from django.contrib import admin

from core.api.v1.forms.indexed_file import IndexedFilerForm
from core.api.v1.models.indexed_file import IndexedFileModel


class IndexedFilerAdmin(admin.ModelAdmin):
    form = IndexedFilerForm
    fields = ['name', 'phone', 'sex', 'birth', 'medical_records_number', 'date_in', 'health_insurance', 'sector',
              'attendance_number', 'uti', 'url']


admin.site.register(IndexedFileModel, IndexedFilerAdmin)
