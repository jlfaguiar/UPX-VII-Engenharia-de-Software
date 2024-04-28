import django.urls
from django.db import models

from django.conf import settings

import django.urls as durls

# Create your models here.
class UsuarioMotorista(models.Model):

    cnh = models.IntegerField(max_length=12)
    nome = models.CharField(max_length=100)
    ra = models.IntegerField(max_length=6)
    telefone = models.CharField(max_length=15)
    id_user = models.CharField(max_length=28)

    def __str__(self):

        return self.nome

    def get_absolute_url(self):

        return durls.reverse('usuario-motorista-lista')

class UsuarioPassageiro(models.Model):

    nome = models.CharField(max_length=100)
    ra = models.IntegerField(max_length=6)
    telefone = models.CharField(max_length=15)
    id_user = models.CharField(max_length=28, unique=True)
    def __str__(self):

        return self.nome

    def get_absolute_url(self):

        return durls.reverse('usuario-passageiro-lista')