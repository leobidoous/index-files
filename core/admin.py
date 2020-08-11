from django.contrib import admin

from core.api.v1.forms.scrap import ScrapForm
from core.api.v1.models.scrap import ScrapModel


class ScrapAdmin(admin.ModelAdmin):
    form = ScrapForm
    fields = ['name', 'cpf', 'birth', 'medical_records_number', 'medical_records_date', 'url']


admin.site.register(ScrapModel, ScrapAdmin)
