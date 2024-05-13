from rest_framework import serializers

from localizacoes.models import *

class LocalizacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Localizacao
        fields = '__all__'