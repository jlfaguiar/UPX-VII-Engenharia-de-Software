from django.db import models
import django.urls as durls
# Create your models here.

class Localizacao(models.Model):

    localizacao = models.CharField(max_length=50)

    def __str__(self):
        return self.localizacao

    def get_absolute_url(self):

        return durls.reverse('')