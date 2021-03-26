from django.urls import include, path
from rest_framework_nested import routers

from .views import UserViewSet, UserConvenioViewSet, UserEstabelecimentoViewSet

# app_name = 'v1'

router = routers.DefaultRouter()
router.register('usuario', UserViewSet, basename='usuario')
user_router = routers.NestedSimpleRouter(router, 'usuario', lookup='usuario')
user_router.register('estabelecimento', UserEstabelecimentoViewSet, basename='estabelecimento')
user_router.register('convenio', UserConvenioViewSet, basename='convenio')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_router.urls))
]
