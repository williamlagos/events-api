# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-03 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20161003_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cover_image_url',
            field=models.URLField(blank=True, default='', max_length=1024, null=True, verbose_name='URL da imagem de capa'),
        ),
    ]