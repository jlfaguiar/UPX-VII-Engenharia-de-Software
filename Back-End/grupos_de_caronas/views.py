from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response

from grupos_de_caronas.serializers import *
import rest_framework.urls as ruls
import rest_framework.generics as rfg

# Create your views here.
class APINewGrupoDeCarona(rfg.CreateAPIView):

    model = GrupoDeCarona
    serializer_class = GrupoDeCaronaSerializer
    fields = '__all__'

class APIListGrupoDeCarona(rfg.ListAPIView):

    model = GrupoDeCarona
    queryset = GrupoDeCarona.objects.all()
    serializer_class = GrupoDeCaronaSerializer

# class APIDetailedGrupoDeCarona(rfg.RetrieveAPIView):
#
#     model = GrupoDeCarona
#     serializer_class = GrupoDeCaronaSerializer

class APIEditGrupoDeCarona(rfg.UpdateAPIView):

    queryset = GrupoDeCarona.objects.all()
    serializer_class = GrupoDeCaronaSerializer
    lookup_field = 'id_motorista'
    http_method_names = ['put', 'patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()

        if 'id_motorista' in data:
            del data['id_motorista']

        data['id_motorista'] = kwargs.get('id_motorista')

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, )

        return Response(serializer.data)

class APIRemoveGrupoDeCarona(rfg.DestroyAPIView):

    queryset = GrupoDeCarona.objects.all()

    model = GrupoDeCarona
    lookup_field = 'id_motorista'
    success_url = durls.reverse_lazy('api-grupo-de-carona-listar')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        self.perform_destroy(instance)
        return JsonResponse({'message': 'Grupo de Carona removido com sucesso!.'}, status=204)

class APINewAssociacaoDeCarona(rfg.CreateAPIView):
    queryset = AssociacaoDeCarona.objects.all()
    serializer_class = AssociacaoDeCaronaSerializer
    model = AssociacaoDeCarona


class APIListAssociacaoDeCarona(rfg.ListAPIView):

    model = AssociacaoDeCarona
    queryset = AssociacaoDeCarona.objects.all()
    serializer_class = AssociacaoDeCaronaSerializer

# class APIDetailedGrupoDeCarona(rfg.RetrieveAPIView):
#
#     model = GrupoDeCarona
#     serializer_class = GrupoDeCaronaSerializer

# class APIEditAssociacaoDeCarona(rfg.UpdateAPIView):
#
#     queryset = AssociacaoDeCarona.objects.all()
#     serializer_class = AssociacaoDeCaronaSerializer
#     lookup_field = 'id_motorista'
#     http_method_names = ['put', 'patch']
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data = request.data.copy()
#
#         if 'id_motorista' in data:
#             del data['id_motorista']
#
#         data['id_motorista'] = kwargs.get('id_motorista')
#
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer, )
#
#         return Response(serializer.data)

class APIRemoveAssociacaoDeCarona(rfg.DestroyAPIView):

    model = AssociacaoDeCarona
    queryset = AssociacaoDeCarona.objects.all()
    serializer_class = AssociacaoDeCaronaSerializer

    def delete(self, request, *args, **kwargs):
        # Recebe os dados do JSON
        id_passageiro = request.data.get('id_passageiro')
        id_carona = request.data.get('id_carona')

        # Verifica se os IDs foram fornecidos
        if id_passageiro is None or id_carona is None:
            return Response({"mensagem": "id_passageiro e id_carona são campos obrigatórios"}, status=400)

        try:
            # Tenta encontrar e excluir a associação de carona
            associacao = AssociacaoDeCarona.objects.get(id_passageiro=id_passageiro, id_carona=id_carona)
            associacao.delete()
            return Response({"mensagem": "Associação de carona removida com sucesso"}, status=200)
        except AssociacaoDeCarona.DoesNotExist:
            return Response({"mensagem": "Associação de carona não encontrada"}, status=404)