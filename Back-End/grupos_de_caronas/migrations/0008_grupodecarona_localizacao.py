# Generated by Django 3.2 on 2024-05-12 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos_de_caronas', '0007_remove_grupodecarona_localizacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupodecarona',
            name='localizacao',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
