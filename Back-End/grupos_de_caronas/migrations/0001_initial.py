# Generated by Django 3.2 on 2024-04-28 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssociacaoDeCarona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_passageiro', models.CharField(max_length=28, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrupoDeCarona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_motorista', models.CharField(max_length=28, unique=True)),
                ('localizacao', models.CharField(max_length=100, unique=True)),
                ('localizacao_desembarque', models.CharField(max_length=150, unique=True)),
                ('localizacao_embarque', models.CharField(max_length=150, unique=True)),
                ('horario_embarque_ida', models.TimeField()),
                ('horario_embarque_volta', models.TimeField()),
                ('valor', models.FloatField()),
            ],
        ),
    ]
