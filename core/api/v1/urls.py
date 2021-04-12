from django.urls import include, path
from rest_framework_nested import routers

from core.api.v1.views import ArquivoIndexadoViewSet, SetorViewSet, EstabelecimentoViewSet, ConvenioViewSet

# app_name = 'v1'

router = routers.DefaultRouter()
router.register('arquivo_indexado', ArquivoIndexadoViewSet, basename='arquivo_indexado')
router.register('estabelecimento', EstabelecimentoViewSet, basename='estabelecimento')
estabelecimento_router = routers.NestedSimpleRouter(router, 'estabelecimento', lookup='estabelecimento')
estabelecimento_router.register('setor', SetorViewSet, basename='setor')
router.register('convenio', ConvenioViewSet, basename='convenio')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(estabelecimento_router.urls), name='estabelecimento'),
    path('', include('authentication.urls'), name='authentication'),
]
