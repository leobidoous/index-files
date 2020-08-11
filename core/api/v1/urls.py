"""bazar_opcao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers

from core.api.v1.views.scrap import ScrapViewSet
from user.views import UserViewSet

app_name = 'v1'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='Usuários')
router.register('indexes', ScrapViewSet, basename='Indexes')

urlpatterns = [
    path('', include(router.urls), name='endpoints'),
]
