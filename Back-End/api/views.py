import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import generic
from rest_framework.response import Response

from api.models import UsuarioMotorista, UsuarioPassageiro
import django.urls as durls

import rest_framework.generics as rfg

from api.serializers import UsuarioPassageiroSerializer, UsuarioMotoristaSerializer
import rest_framework.generics as rfg

# Create your views here.
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
        return rfg.get_object_or_404(UsuarioMotorista, id_user=id_user)

class RemoveUsuarioMotorista(generic.DeleteView):

    model = UsuarioMotorista

    success_url = durls.reverse_lazy('usuario-motorista-lista')


class NewUsuarioPassageiro(generic.CreateView):

    model = UsuarioPassageiro

    fields = ['nome', 'ra', 'telefone']


class ListUsuarioPassageiro(generic.ListView):

    model = UsuarioPassageiro
    queryset = UsuarioPassageiro.objects.all()


class EditUsuarioPassageiro(generic.UpdateView):

    model = UsuarioPassageiro

    fields = ['nome', 'cnh', 'ra', 'telefone']
    template_name_suffix = '_update_form'


class DetailedUsuarioPassageiro(generic.DetailView):

    model = UsuarioPassageiro


class RemoveUsuarioPassageiro(generic.DeleteView):

    model = UsuarioPassageiro

    success_url = durls.reverse_lazy('usuario-motorista-lista')


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

class APINewUsuarioMotorista(rfg.CreateAPIView):

    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    fields = ['nome', 'cnh', 'ra', 'telefone']

class APIListUsuarioMotorista(rfg.ListAPIView):

    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    queryset = UsuarioMotorista.objects.all()


class APIEditUsuarioMotorista(rfg.UpdateAPIView):

    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    fields = ['nome', 'cnh', 'ra', 'telefone']
    template_name_suffix = '_update_form'


class APIDetailedUsuarioMotorista(rfg.RetrieveAPIView):

    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer

    def get_object(self):

        id_user = self.kwargs.get('id_user')
        return rfg.get_object_or_404(UsuarioMotorista, id_user=id_user)


class APIRemoveUsuarioMotorista(rfg.DestroyAPIView):

    model = UsuarioMotorista
    serializer_class = UsuarioMotoristaSerializer
    success_url = durls.reverse_lazy('usuario-motorista-lista')

class APINewUsuarioPassageiro(rfg.CreateAPIView):

    model = UsuarioPassageiro
    serializer_class = UsuarioPassageiroSerializer
    fields = ['nome', 'ra', 'telefone']

class APIListUsuarioPassageiro(rfg.ListAPIView):
    model = UsuarioPassageiro
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer

class APIDetailedUsuarioPassageiro(rfg.RetrieveAPIView):

    model = UsuarioPassageiro
    serializer_class = UsuarioPassageiroSerializer

    def get_object(self):
        id_user = self.kwargs.get('id_user')
        print(self.kwargs)
        return rfg.get_object_or_404(UsuarioPassageiro, id_user=id_user)
class APIEditUsuarioPassageiro(rfg.UpdateAPIView):
    queryset = UsuarioPassageiro.objects.all()
    serializer_class = UsuarioPassageiroSerializer
    lookup_field = 'id_user'
    http_method_names = ['put', 'patch']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()  # Copying data to prevent modifying original data

        # Remove 'id_user' field from data if present to prevent editing it
        if 'id_user' in data:
            del data['id_user']

        data['id_user'] = kwargs.get('id_user')

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, )

        return Response(serializer.data)

class APIRemoveUsuarioPassageiro(rfg.DestroyAPIView):

    queryset = UsuarioPassageiro.objects.all()

    model = UsuarioPassageiro
    lookup_field = 'id_user'
    success_url = durls.reverse_lazy('usuario-passageiro-lista')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'message': 'Usuário motorista removido com sucesso.'}, status=204)