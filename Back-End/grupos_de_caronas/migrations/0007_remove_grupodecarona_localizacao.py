# Generated by Django 3.2 on 2024-05-12 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grupos_de_caronas', '0006_grupodecarona_id_localizacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupodecarona',
            name='localizacao',
        ),
    ]
