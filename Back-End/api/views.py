from django.shortcuts import render, get_object_or_404
from django.views import generic

from api.models import UsuarioMotorista, UsuarioPassageiro
import django.urls as durls

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
