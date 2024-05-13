from django.shortcuts import render
import rest_framework.generics as rfg
from localizacoes.models import *
from localizacoes.serializers import *
# Create your views here.

class APIListLocalizacoes(rfg.ListAPIView):

    model = Localizacao
    queryset = Localizacao.objects.all()
    serializer_class = LocalizacaoSerializer