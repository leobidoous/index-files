"""Omni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

namespace = 'authentication'

urlpatterns = [
    path(r'auth/login/', obtain_jwt_token, name='login'),
    path(r'auth/refresh-token/', refresh_jwt_token, name='refresh_jwt_token'),
    path(r'auth/api-token-verify/', verify_jwt_token, name='verify_jwt_token'),
]
