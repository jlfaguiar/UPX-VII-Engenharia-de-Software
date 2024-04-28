from rest_framework import serializers
from api.models import UsuarioPassageiro, UsuarioMotorista

class UsuarioPassageiroSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuarioPassageiro
        fields = '__all__'

class UsuarioMotoristaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuarioMotorista
        fields = '__all__'
