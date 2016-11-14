# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-03 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0002_auto_20161003_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='parent_property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meta_properties', to='designer.Property'),
        ),
    ]