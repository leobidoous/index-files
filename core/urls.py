"""indexes URL Configuration

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
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('administracao/', views.AdministradorView.as_view(), name="administrador"),
    path('api/', include('core.api.urls')),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path('login/', LoginView.as_view(template_name='core/base_login.html'), name='login'),
    path('redefinir-senha', views.SolicitarRedefinirSenha.as_view(), name='reset_password'),
    path('redefinir-senha/done', views.RedefinirSenhaCompleto.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', views.RedefinirSenha.as_view(), name='password_reset_confirm'),
]
