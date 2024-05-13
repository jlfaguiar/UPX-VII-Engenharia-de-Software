from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from grupos_de_caronas.models import *
from localizacoes.models import *
from api.models import UsuarioMotorista

class GrupoDeCaronaSerializer(serializers.ModelSerializer):

    nome_motorista = serializers.SerializerMethodField()
    telefone_motorista = serializers.SerializerMethodField()
    carona_participante = serializers.SerializerMethodField()
    total_passageiros = serializers.SerializerMethodField()
    localizacao = serializers.SerializerMethodField()
    class Meta:
        model = GrupoDeCarona
        fields = '__all__'

    def to_representation(self, instance):

        data = super().to_representation(instance)

        id_usuario = self.context['request'].resolver_match.kwargs.get('id_usuario')

        if 'id_motorista' in data.keys():
            data['minha_carona'] = data['id_motorista'] == str(id_usuario)
        else:
            data['minha_carona'] = False

        data.pop('id_motorista', None)  # Remove o campo id_motorista

        return data

    def get_nome_motorista(self, obj):
        motorista = get_object_or_404(UsuarioMotorista, id_user=obj.id_motorista)
        return motorista.nome

    def get_telefone_motorista(self, obj):
        motorista = get_object_or_404(UsuarioMotorista, id_user=obj.id_motorista)
        return motorista.telefone

    def get_carona_participante(self, obj):

        id_usuario = self.context['request'].resolver_match.kwargs.get('id_usuario')
        associacao = AssociacaoDeCarona.objects.filter(id_carona_id=obj.id, id_passageiro=id_usuario).exists()
        return associacao

    def get_total_passageiros(self, obj):

        associacoes = AssociacaoDeCarona.objects.filter(id_carona_id=obj.id)
        return len(associacoes)

    def get_localizacao(self, obj):

        return obj.id_localizacao.localizacao

class AssociacaoDeCaronaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssociacaoDeCarona
        fields = '__all__'

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data.pop('id_passageiro', None)  # Remove o campo id_motorista

        return data
