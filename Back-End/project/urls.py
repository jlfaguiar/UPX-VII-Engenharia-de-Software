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
from django.urls import path, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from api.views import *
from grupos_de_caronas.views import *
from localizacoes.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="API do FACENS Caronas",
      default_version='v1',
      description="Documentação da API do FACENS Caronas usando Swagger",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jlfaguiar@outlook.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/usuariomotorista/novo/', APINewUsuarioMotorista.as_view(), name='api-usuario-motorista-novo'),
    path('api/usuariopassageiro/novo/', APINewUsuarioPassageiro.as_view(), name='api-usuario-passageiro-novo'),

    # path('api/usuariopassageiro/<str:id_user>/editar', APIEditUsuarioPassageiro.as_view(),
    #      name='api-usuario-passageiro-editar'),
    # path('api/usuariopassageiro/<str:id_user>/apagar', APIRemoveUsuarioPassageiro.as_view(),
    #      name='api-usuario-passageiro-apagar'),

    path('api/usuariopassageiro/<str:id_user>/detalhar/', APIDetailedUsuarioPassageiro.as_view(),
         name='api-usuario-passageiro-detalhar'),
    path('api/usuariomotorista/<str:id_user>/detalhar/', APIDetailedUsuarioMotorista.as_view(),
         name='api-usuario-motorista-detalhar'),

    path('api/grupodecarona/novo', APINewGrupoDeCarona.as_view(), name='api-grupo-de-carona-novo'),
    path('api/grupodecarona/<str:id_usuario>/lista/', APIListGrupoDeCarona.as_view(),
         name='api-grupo-de-carona-listar'),
    path('api/grupodecarona/<int:id>/editar', APIEditGrupoDeCarona.as_view(),
         name='api-grupo-de-carona-editar'),
    path('api/grupodecarona/<str:id_user>/apagar', APIRemoveGrupoDeCarona.as_view(),
         name='api-grupo-de-carona-apagar'),

    path('api/associacaodecarona/novo', APINewAssociacaoDeCarona.as_view(),
         name='api-associacao-de-carona-novo'),
    path('api/associacaodecarona/<str:id_passageiro>/<int:id_carona>/apagar', APIRemoveAssociacaoDeCarona.as_view(),
         name='api-associacao-de-carona-apagar'),

    path('api/localizacoes', APIListLocalizacoes.as_view(), name='api-localizacoes-listar'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

