# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-24 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ImageEditor', '0004_auto_20160624_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefunction',
            name='function_type',
            field=models.CharField(
                choices=[('1', 'Transform'), ('2', 'ColorTint'), ('3', 'Adjustment'), ('4', 'ColorFilter'),
                         ('5', 'KernelFilter')], max_length=15),
        ),
    ]