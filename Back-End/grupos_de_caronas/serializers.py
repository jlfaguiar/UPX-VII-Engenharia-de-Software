from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from grupos_de_caronas.models import GrupoDeCarona, AssociacaoDeCarona
from localizacoes.models import Localizacao
from api.models import UsuarioMotorista

# Classe dedicada a extrair as informações dos motoristas
class MotoristaHelper:

    @staticmethod
    def obter_nome_motorista(id_motorista):
        motorista = get_object_or_404(UsuarioMotorista, id_user=id_motorista)
        return motorista.nome

    @staticmethod
    def obter_telefone_motorista(id_motorista):
        motorista = get_object_or_404(UsuarioMotorista, id_user=id_motorista)
        return motorista.telefone

# Classe dedicada a preparar as informações antes de finalizar a serialização
class GrupoDeCaronaRepresentationHelper:

    @staticmethod
    def preparar_dados(instance, context):
        data = instance
        id_usuario = context['request'].resolver_match.kwargs.get('id_usuario')

        data['minha_carona'] = data.get('id_motorista') == str(id_usuario)
        data.pop('id_motorista', None)  # Remove o campo id_motorista
        return data

# Classe serializadora, dedicada
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
        return GrupoDeCaronaRepresentationHelper.preparar_dados(data, self.context)

    def get_nome_motorista(self, obj):
        return MotoristaHelper.obter_nome_motorista(obj.id_motorista)

    def get_telefone_motorista(self, obj):
        return MotoristaHelper.obter_telefone_motorista(obj.id_motorista)

    def get_carona_participante(self, obj):
        id_usuario = self._obter_id_usuario()
        return AssociacaoDeCarona.objects.filter(id_carona_id=obj.id, id_passageiro=id_usuario).exists()

    def get_total_passageiros(self, obj):
        return AssociacaoDeCarona.objects.filter(id_carona_id=obj.id).count()

    def get_localizacao(self, obj):
        return obj.id_localizacao.localizacao

    def _obter_id_usuario(self):
        return self.context['request'].resolver_match.kwargs.get('id_usuario')

class AssociacaoDeCaronaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssociacaoDeCarona
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('id_passageiro', None)  # Remove o campo id_passageiro
        return data
