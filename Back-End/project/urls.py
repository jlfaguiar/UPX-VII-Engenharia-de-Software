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

from api.views import *
from grupos_de_caronas.views import *

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

    path('api/usuariomotorista/novo/', APINewUsuarioMotorista.as_view(), name='api-usuario-motorista-novo'),

    path('api/usuariopassageiro/novo/', APINewUsuarioPassageiro.as_view(), name='api-usuario-passageiro-novo'),
    # path('api/usuariopassageiro/lista/', APIListUsuarioPassageiro.as_view(), name='api-usuario-passageiro-listar'),
    path('api/usuariopassageiro/<str:id_user>/editar', APIEditUsuarioPassageiro.as_view(),
         name='api-usuario-passageiro-editar'),
    path('api/usuariopassageiro/<str:id_user>/apagar', APIRemoveUsuarioPassageiro.as_view(),
         name='api-usuario-passageiro-apagar'),

    path('api/grupodecarona/novo', APINewGrupoDeCarona.as_view(), name='api-grupo-de-carona-novo'),
    path('api/grupodecarona/<str:id_motorista>/lista/', APIListGrupoDeCarona.as_view(),
         name='api-grupo-de-carona-listar'),
    path('api/grupodecarona/<str:id_motorista>/editar', APIEditUsuarioPassageiro.as_view(),
         name='api-grupo-de-carona-editar'),
    path('api/grupodecarona/<str:id_user>/apagar', APIRemoveGrupoDeCarona.as_view(), name='api-grupo-de-carona-apagar'),

    path('api/associacaodecarona/novo', APINewGrupoDeCarona.as_view(), name='api-associacao-de-carona-novo'),
    # path('api/associacaodecarona/<str:id_motorista>/lista/', APIListGrupoDeCarona.as_view(),
    #      name='api-grupo-de-carona-listar'),
    # path('api/associacaodecarona/<str:id_motorista>/editar', APIEditUsuarioPassageiro.as_view(),
    #      name='api-grupo-de-carona-editar'),
    path('api/associacaodecarona/<str:id_passageiro>/<int:fk>/apagar', APIRemoveGrupoDeCarona.as_view(),
         name='api-associacao-de-carona-apagar'),

]

