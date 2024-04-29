from django.db import models
import django.urls as durls

class GrupoDeCarona(models.Model):

    id_motorista = models.CharField(max_length=28)

    localizacao = models.CharField(max_length=100, unique=False)
    localizacao_desembarque = models.CharField(max_length=150, unique=False)
    localizacao_embarque = models.CharField(max_length=150, unique=False)

    horario_embarque_ida = models.TimeField()
    horario_embarque_volta = models.TimeField()

    valor = models.FloatField()
    def __str__(self):

        return self.id_motorista

    def get_absolute_url(self):

        return durls.reverse('')

class AssociacaoDeCarona(models.Model):

    id_carona = models.ForeignKey(on_delete=models.CASCADE, to=GrupoDeCarona, unique=False)
    id_passageiro = models.CharField(max_length=28, unique=False)

    def __str__(self):

        return str(self.id_carona)

    def get_absolute_url(self):

        return durls.reverse('')