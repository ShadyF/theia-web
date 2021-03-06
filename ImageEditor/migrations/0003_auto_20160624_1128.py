# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-24 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ImageEditor', '0002_colorfilterfunction_kernelfilterfunction_transformfunction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colorfilterfunction',
            name='display_name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='kernelfilterfunction',
            name='display_name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='transformfunction',
            name='display_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
