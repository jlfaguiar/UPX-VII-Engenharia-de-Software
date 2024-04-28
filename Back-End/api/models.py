import django.urls
from django.db import models

from django.conf import settings
from  django.contrib.auth.models import AbstractUser

import django.urls as durls

# Create your models here.
class UsuarioMotorista(models.Model):

    cnh = models.PositiveSmallIntegerField()
    nome = models.CharField(max_length=100)
    ra = models.PositiveSmallIntegerField()
    telefone = models.CharField(max_length=15)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):

        return self.nome

    def get_absolute_url(self):

        return durls.reverse('usuario-motorista-lista')

class UsuarioPassageiro(models.Model):

    nome = models.CharField(max_length=100)
    ra = models.PositiveSmallIntegerField()
    telefone = models.CharField(max_length=15)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):

        return self.nome

