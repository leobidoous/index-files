from django.urls import include, path
from rest_framework import routers

from user.views import UserViewSet

app_name = 'v1'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='Usuários')

urlpatterns = [
    path('', include(router.urls), name='endpoints'),
    path('', include('authentication.urls'), name='authentication'),
]
