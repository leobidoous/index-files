from django.urls import path

from .views import search_document

app_name = 'edok'

urlpatterns = [
    path('buscar_documento/', search_document, name='buscar_documento')
]
