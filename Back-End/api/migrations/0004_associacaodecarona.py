# Generated by Django 3.2 on 2024-04-28 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_grupodecarona'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociacaoDeCarona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_passageiro', models.CharField(max_length=28, unique=True)),
            ],
        ),
    ]
