from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from grupos_de_caronas.models import *
from api.models import UsuarioMotorista

class GrupoDeCaronaSerializer(serializers.ModelSerializer):

    nome_motorista = serializers.SerializerMethodField()
    telefone_motorista = serializers.SerializerMethodField()

    class Meta:
        model = GrupoDeCarona
        fields = '__all__'

    def to_representation(self, instance):

        data = super().to_representation(instance)

        data['minha_carona'] = data['id_motorista'] == str(instance)
        data.pop('id_motorista', None)  # Remove o campo id_motorista

        return data

    def get_nome_motorista(self, obj):
        motorista = get_object_or_404(UsuarioMotorista, id_user=obj.id_motorista)
        return motorista.nome

    def get_telefone_motorista(self, obj):
        motorista = get_object_or_404(UsuarioMotorista, id_user=obj.id_motorista)
        return motorista.telefone

class AssociacaoDeCaronaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssociacaoDeCarona
        fields = '__all__'
