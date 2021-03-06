# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-24 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ImageEditor', '0003_auto_20160624_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=30, unique=True)),
                ('function_name', models.CharField(max_length=30)),
                ('function_type', models.CharField(
                    choices=[('1', 'Transform'), ('2', 'ColorFilter'), ('3', 'KernelFilter'), ('4', 'ColorTint')],
                    max_length=15)),
            ],
        ),
        migrations.DeleteModel(
            name='ColorFilterFunction',
        ),
        migrations.DeleteModel(
            name='KernelFilterFunction',
        ),
        migrations.DeleteModel(
            name='TransformFunction',
        ),
    ]
