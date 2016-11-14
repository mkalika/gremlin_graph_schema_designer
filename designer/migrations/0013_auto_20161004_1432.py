# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-04 11:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0012_schema_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metaproperty',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message="Property name doesn't comply", regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$')]),
        ),
    ]