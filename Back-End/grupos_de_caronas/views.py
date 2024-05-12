from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from django.http import Http404
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

    def get_object(self):
        id_passageiro = self.kwargs.get('id_passageiro')
        id_carona = self.kwargs.get('id_carona')

        try:
            return self.queryset.get(id_passageiro=id_passageiro, id_carona=id_carona)
        except AssociacaoDeCarona.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)