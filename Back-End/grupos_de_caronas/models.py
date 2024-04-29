from django.db import models
import django.urls as durls

class GrupoDeCarona(models.Model):

    id_motorista = models.CharField(max_length=28, unique=True)

    localizacao = models.CharField(max_length=100, unique=True)
    localizacao_desembarque = models.CharField(max_length=150, unique=True)
    localizacao_embarque = models.CharField(max_length=150, unique=True)

    horario_embarque_ida = models.TimeField()
    horario_embarque_volta = models.TimeField()

    valor = models.FloatField()
    def __str__(self):

        return self.id_motorista

    def get_absolute_url(self):

        return durls.reverse('')

class AssociacaoDeCarona(models.Model):

    id_carona: models.ForeignKey(on_delete=models.CASCADE, to=GrupoDeCarona, null=None)
    id_passageiro = models.CharField(max_length=28, unique=True)

    def __str__(self):

        return 'Associação de Grupo de Caronas Genérico'

    def get_absolute_url(self):

        return durls.reverse('')