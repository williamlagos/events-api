# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-25 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowley', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='action',
            field=models.CharField(choices=[('A', 'Permitir'), ('D', 'Proibir')], default='A', max_length=1, verbose_name='Ação'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Ativa'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='content',
            field=models.CharField(max_length=255, verbose_name='Conteúdo'),
        ),
    ]
