# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-25 17:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20160802_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_time', 'name']},
        ),
    ]
