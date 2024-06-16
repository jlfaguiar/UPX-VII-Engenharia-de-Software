import json
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from api.models import UsuarioMotorista, UsuarioPassageiro
from api.serializers import UsuarioPassageiroSerializer, UsuarioMotoristaSerializer

# Serviço para manipulação de UsuarioMotorista
class UsuarioMotoristaService:
    @staticmethod
    def criar_motorista(data):
        return UsuarioMotorista.objects.create(**data)

    @staticmethod
    def obter_motorista(id_user):
        return get_object_or_404(UsuarioMotorista, id_user=id_user)

# Serviço para manipulação de UsuarioPassageiro
class UsuarioPassageiroService:
    @staticmethod
    def criar_passageiro(data):
        return UsuarioPassageiro.objects.create(**data)

    @staticmethod
    def obter_passageiro(id_user):
        return get_object_or_404(UsuarioPassageiro, id_user=id_user)

# SRP: Views para UsuarioMotorista

class NewUsuarioMotorista(generic.CreateView):
    model = UsuarioMotorista
    fields = ['nome', 'cnh', 'ra', 'telefone']

class ListUsuarioMotorista(generic.ListView):
    model = UsuarioMotorista
    queryset = UsuarioMotorista.objects.all()

class EditUsuarioMotorista(generic.UpdateView):
    model = UsuarioMotorista
    fields = ['nome', 'cnh', 'ra', 'telefone']
    template_name_suffix = '_update_form'

class DetailedUsuarioMotorista(generic.DetailView):
    model = UsuarioMotorista

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        return UsuarioMotoristaService.obter_motorista(id_user)

class RemoveUsuarioMotorista(generic.DeleteView):
    model = UsuarioMotorista
    success_url = reverse_lazy('usuario-motorista-lista')

# SRP: Views para UsuarioPassageiro

class NewUsuarioPassageiro(generic.CreateView):
    model = UsuarioPassageiro
    fields = ['nome', 'ra', 'telefone']

class ListUsuarioPassageiro(generic.ListView):
    model = UsuarioPassageiro
    queryset = UsuarioPassageiro.objects.all()

class EditUsuarioPassageiro(generic.UpdateView):
    model = UsuarioPassageiro
    fields = ['nome', 'ra', 'telefone']
    template_name_suffix = '_update_form'

class DetailedUsuarioPassageiro(generic.DetailView):
    model = UsuarioPassageiro

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        return UsuarioPassageiroService.obter_passageiro(id_user)

class RemoveUsuarioPassageiro(generic.DeleteView):
    model = UsuarioPassageiro
    success_url = reverse_lazy('usuario-passageiro-lista')

# SRP: View para criação de novos usuários

class NewUsuario(generic.CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        d_request = json.loads(request.body.decode('utf-8'))
        username = d_request['username']
        password = d_request['password']
        email = d_request['email']
        is_driver = d_request['is_driver']

        try:
            user = User.objects.create_user(email=email, password=password, username=username)
        except Exception as error:
            return JsonResponse({'message': 'Erro ao criar usuário: {}'.format(str(error))}, status=400)

        user_data = {
            'nome': d_request['nome'],
            'ra': d_request['ra'],
            'telefone': d_request['telefone'],
            'id_user': user.id
        }

        if is_driver:
            UsuarioMotoristaService.criar_motorista(user_data)
        else:
            UsuarioPassageiroService.criar_passageiro(user_data)

        return JsonResponse({'message': 'Usuário criado com sucesso'}, status=201)

# OCP: API Views para UsuarioMotorista

class APINewUsuarioMotorista(generics.CreateAPIView):
    queryset = UsuarioMotorista.objects.all()
    serializer_class = UsuarioMotoristaSerializer

class APIListUsuarioMotorista(generics.ListAPIView):
    queryset = UsuarioMotorista.objects.all()
    serializer_class = UsuarioMotoristaSerializer

class APIEditUsuarioMotorista(generics.UpdateAPIView):
    queryset = UsuarioMotorista.objects.all()
    serializer_class = UsuarioMotoristaSerializer

class APIDetailedUsuarioMotorista(generics.RetrieveAPIView):
    queryset = UsuarioMotorista.objects.all()
    serializer_class = UsuarioMotoristaSerializer

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        return UsuarioMotoristaService.obter_motorista(id_user)

class APIRemoveUsuarioMotorista(generics.DestroyAPIView):
    queryset = UsuarioMotorista.objects.all()
    serializer_class = UsuarioMotoristaSerializer
    success_url = reverse_lazy('usuario-motorista-lista')

# OCP: API Views para UsuarioPassageiro

class APINewUsuarioPassageiro(generics.CreateAPIView):
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer

class APIListUsuarioPassageiro(generics.ListAPIView):
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer

class APIEditUsuarioPassageiro(generics.UpdateAPIView):
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer
    lookup_field = 'id_user'
    http_method_names = ['put', 'patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()

        if 'id_user' in data:
            del data['id_user']

        data['id_user'] = kwargs.get('id_user')

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class APIDetailedUsuarioPassageiro(generics.RetrieveAPIView):
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        return UsuarioPassageiroService.obter_passageiro(id_user)

class APIRemoveUsuarioPassageiro(generics.DestroyAPIView):
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer
    lookup_field = 'id_user'
    success_url = reverse_lazy('usuario-passageiro-lista')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'message': 'Usuário passageiro removido com sucesso.'}, status=204)
