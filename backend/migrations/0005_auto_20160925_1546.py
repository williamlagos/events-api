# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-25 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20160925_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='event',
            name='attending_count',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Confirmados'),
        ),
        migrations.AlterField(
            model_name='event',
            name='city_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='event',
            name='cover_image_url',
            field=models.URLField(blank=True, default='', max_length=1024, verbose_name='URL da imagem de capa'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Término'),
        ),
        migrations.AlterField(
            model_name='event',
            name='external_id',
            field=models.CharField(max_length=50, unique=True, verbose_name='ID Externo'),
        ),
        migrations.AlterField(
            model_name='event',
            name='interested_count',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Interessados'),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_page_owned',
            field=models.BooleanField(default=False, verbose_name='Criado por Página'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(verbose_name='Início'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='external_id',
            field=models.CharField(max_length=50, unique=True, verbose_name='ID Externo'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='external_type',
            field=models.CharField(max_length=50, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='status',
            field=models.CharField(max_length=1, verbose_name='Status'),
        ),
    ]
