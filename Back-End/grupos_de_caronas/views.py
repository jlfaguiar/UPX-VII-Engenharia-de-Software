from django.http import JsonResponse, Http404
from rest_framework.response import Response
from rest_framework import generics
from grupos_de_caronas.serializers import GrupoDeCaronaSerializer, AssociacaoDeCaronaSerializer
from grupos_de_caronas.models import GrupoDeCarona, AssociacaoDeCarona
from django.urls import reverse_lazy

# Serviço para manipular GrupoDeCarona
class GrupoDeCaronaService:
    @staticmethod
    def verificar_motorista(grupo, id_motorista):
        if id_motorista and id_motorista != grupo.id_motorista:
            return False
        return True

# Serviço para manipular AssociacaoDeCarona
class AssociacaoDeCaronaService:
    @staticmethod
    def obter_associacao(queryset, id_passageiro, id_carona):
        try:
            return queryset.get(id_passageiro=id_passageiro, id_carona=id_carona)
        except AssociacaoDeCarona.DoesNotExist:
            raise Http404

class APINewGrupoDeCarona(generics.CreateAPIView):
    model = GrupoDeCarona
    serializer_class = GrupoDeCaronaSerializer
    fields = '__all__'

class APIListGrupoDeCarona(generics.ListAPIView):
    model = GrupoDeCarona
    queryset = GrupoDeCarona.objects.all()
    serializer_class = GrupoDeCaronaSerializer

class APIEditGrupoDeCarona(generics.UpdateAPIView):
    queryset = GrupoDeCarona.objects.all()
    serializer_class = GrupoDeCaronaSerializer
    lookup_field = 'id'
    http_method_names = ['put', 'patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Verificação de id_motorista
        id_motorista = request.data.get('id_motorista')
        if not GrupoDeCaronaService.verificar_motorista(instance, id_motorista):
            return Response({"error": "Motorista não corresponde ao grupo de carona"}, status=400)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class APIRemoveGrupoDeCarona(generics.DestroyAPIView):
    queryset = GrupoDeCarona.objects.all()
    lookup_field = 'id_motorista'
    success_url = reverse_lazy('api-grupo-de-carona-listar')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'message': 'Grupo de Carona removido com sucesso!'}, status=204)

class APINewAssociacaoDeCarona(generics.CreateAPIView):

    queryset = AssociacaoDeCarona.objects.all()
    serializer_class = AssociacaoDeCaronaSerializer
    model = AssociacaoDeCarona

class APIListAssociacaoDeCarona(generics.ListAPIView):

    model = AssociacaoDeCarona
    queryset = AssociacaoDeCarona.objects.all()
    serializer_class = AssociacaoDeCaronaSerializer

class APIRemoveAssociacaoDeCarona(generics.DestroyAPIView):

    model = AssociacaoDeCarona
    queryset = AssociacaoDeCarona.objects.all()
    serializer_class = AssociacaoDeCaronaSerializer

    def get_object(self):
        id_passageiro = self.kwargs.get('id_passageiro')
        id_carona = self.kwargs.get('id_carona')
        return AssociacaoDeCaronaService.obter_associacao(self.queryset, id_passageiro, id_carona)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)