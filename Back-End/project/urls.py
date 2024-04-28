"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from api.views import NewUsuarioMotorista, EditUsuarioMotorista, ListUsuarioMotorista, DetailedUsuarioMotorista, \
    RemoveUsuarioMotorista

from api.views import NewUsuarioPassageiro, ListUsuarioPassageiro, EditUsuarioPassageiro, DetailedUsuarioPassageiro, \
    RemoveUsuarioPassageiro


urlpatterns = [
    path('admin/', admin.site.urls),

    path('usuariomotorista/novo/', NewUsuarioMotorista.as_view(), name='usuario-motorista-novo'),
    path('usuariomotorista/lista/', ListUsuarioMotorista.as_view(), name='usuario-motorista-lista'),
    path('usuariomotorista/<int:pk>/editar/', EditUsuarioMotorista.as_view(), name='usuario-motorista-editar'),
    path('usuariomotorista/<int:pk>/detalhar/', DetailedUsuarioMotorista.as_view(), name='usuario-motorista-detalhar'),
    path('usuariomotorista/<int:pk>/apagar/', RemoveUsuarioMotorista.as_view(), name='usuario-motorista-apagar'),

    path('usuariopassageiro/novo/', NewUsuarioPassageiro.as_view(), name='usuario-passageiro-novo'),
    path('usuariopassageiro/lista/', ListUsuarioPassageiro.as_view(), name='usuario-passageiro-lista'),
    path('usuariopassageiro/<int:pk>/editar/', EditUsuarioPassageiro.as_view(), name='usuario-passageiro-editar'),
    path('usuariopassageiro/<int:pk>/detalhar/', DetailedUsuarioPassageiro.as_view(),
         name='usuario-passageiro-detalhar'),
    path('usuariopassageiro/<int:pk>/apagar/', RemoveUsuarioPassageiro.as_view(), name='usuario-passageiro-apagar'),

]

