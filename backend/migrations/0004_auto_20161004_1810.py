# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-04 21:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20161004_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='city_name',
        ),
        migrations.RemoveField(
            model_name='event',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='event',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='external_type',
        ),
        migrations.RemoveField(
            model_name='owner',
            name='status',
        ),
    ]