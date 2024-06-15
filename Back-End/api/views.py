import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from api.models import UsuarioMotorista, UsuarioPassageiro
from api.serializers import UsuarioPassageiroSerializer, UsuarioMotoristaSerializer

# SRP: Classes para manipulação de UsuarioMotorista

class NewUsuarioMotorista(generic.CreateView):
    model = UsuarioMotorista
    fields = ['nome', 'cnh', 'ra', 'telefone']
    # SRP: Responsável apenas por criar um novo UsuarioMotorista

class ListUsuarioMotorista(generic.ListView):
    model = UsuarioMotorista
    queryset = UsuarioMotorista.objects.all()
    # SRP: Responsável apenas por listar UsuarioMotorista

class EditUsuarioMotorista(generic.UpdateView):
    model = UsuarioMotorista
    fields = ['nome', 'cnh', 'ra', 'telefone']
    template_name_suffix = '_update_form'
    # SRP: Responsável apenas por editar um UsuarioMotorista

class DetailedUsuarioMotorista(generic.DetailView):
    model = UsuarioMotorista

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        return get_object_or_404(UsuarioMotorista, id_user=id_user)
    # SRP: Responsável apenas por detalhar um UsuarioMotorista

class RemoveUsuarioMotorista(generic.DeleteView):
    model = UsuarioMotorista
    success_url = reverse_lazy('usuario-motorista-lista')
    # SRP: Responsável apenas por remover um UsuarioMotorista

# SRP: Classes para manipulação de UsuarioPassageiro

class NewUsuarioPassageiro(generic.CreateView):
    model = UsuarioPassageiro
    fields = ['nome', 'ra', 'telefone']
    # SRP: Responsável apenas por criar um novo UsuarioPassageiro

class ListUsuarioPassageiro(generic.ListView):
    model = UsuarioPassageiro
    queryset = UsuarioPassageiro.objects.all()
    # SRP: Responsável apenas por listar UsuarioPassageiro

class EditUsuarioPassageiro(generic.UpdateView):
    model = UsuarioPassageiro
    fields = ['nome', 'ra', 'telefone']
    template_name_suffix = '_update_form'
    # SRP: Responsável apenas por editar um UsuarioPassageiro

class DetailedUsuarioPassageiro(generic.DetailView):
    model = UsuarioPassageiro
    # SRP: Responsável apenas por detalhar um UsuarioPassageiro

class RemoveUsuarioPassageiro(generic.DeleteView):
    model = UsuarioPassageiro
    success_url = reverse_lazy('usuario-passageiro-lista')
    # SRP: Responsável apenas por remover um UsuarioPassageiro

# SRP: Classe para criação de novos usuários

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

        return NewUsuarioMotorista.as_view()(request) if is_driver else NewUsuarioPassageiro.as_view()(request)
    # SRP: Responsável apenas pela criação de um novo usuário e delegação da criação de um UsuarioMotorista ou UsuarioPassageiro

# OCP: API Views para UsuarioMotorista

class APINewUsuarioMotorista(generics.CreateAPIView):
    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    # OCP: Aberto para extensão, fechado para modificação. Adiciona um novo UsuarioMotorista

class APIListUsuarioMotorista(generics.ListAPIView):
    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    queryset = UsuarioMotorista.objects.all()
    # OCP: Aberto para extensão, fechado para modificação. Lista UsuarioMotorista

class APIEditUsuarioMotorista(generics.UpdateAPIView):
    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    # OCP: Aberto para extensão, fechado para modificação. Edita um UsuarioMotorista

class APIDetailedUsuarioMotorista(generics.RetrieveAPIView):
    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        return get_object_or_404(UsuarioMotorista, id_user=id_user)
    # OCP: Aberto para extensão, fechado para modificação. Detalha um UsuarioMotorista

class APIRemoveUsuarioMotorista(generics.DestroyAPIView):
    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    success_url = reverse_lazy('usuario-motorista-lista')
    # OCP: Aberto para extensão, fechado para modificação. Remove um UsuarioMotorista

# OCP: API Views para UsuarioPassageiro

class APINewUsuarioPassageiro(generics.CreateAPIView):
    model = UsuarioPassageiro
    serializer_class = UsuarioPassageiroSerializer
    # OCP: Aberto para extensão, fechado para modificação. Adiciona um novo UsuarioPassageiro

class APIListUsuarioPassageiro(generics.ListAPIView):
    model = UsuarioPassageiro
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer
    # OCP: Aberto para extensão, fechado para modificação. Lista UsuarioPassageiro

class APIDetailedUsuarioPassageiro(generics.RetrieveAPIView):
    model = UsuarioPassageiro
    serializer_class = UsuarioPassageiroSerializer

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        return get_object_or_404(UsuarioPassageiro, id_user=id_user)
    # OCP: Aberto para extensão, fechado para modificação. Detalha um UsuarioPassageiro

class APIEditUsuarioPassageiro(generics.UpdateAPIView):
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer
    lookup_field = 'id_user'
    http_method_names = ['put', 'patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()

        # Remove 'id_user' field from data if present to prevent editing it
        if 'id_user' in data:
            del data['id_user']

        data['id_user'] = kwargs.get('id_user')

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    # OCP: Aberto para extensão, fechado para modificação. Edita um UsuarioPassageiro

class APIRemoveUsuarioPassageiro(generics.DestroyAPIView):
    queryset = UsuarioPassageiro.objects.all()
    model = UsuarioPassageiro
    lookup_field = 'id_user'
    success_url = reverse_lazy('usuario-passageiro-lista')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'message': 'Usuário passageiro removido com sucesso.'}, status=204)
    # OCP: Aberto para extensão, fechado para modificação. Remove um UsuarioPassageiro
