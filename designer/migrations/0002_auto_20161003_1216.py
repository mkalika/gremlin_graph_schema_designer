# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-03 12:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edgelabel',
            name='label',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message="Vertex label doesn't comply", regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$')]),
        ),
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message="Property name doesn't comply", regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$')]),
        ),
        migrations.AlterField(
            model_name='schema',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vertexlabel',
            name='label',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message="Vertex label doesn't comply", regex='^[a-zA-Z_$][a-zA-Z_$0-9]*$')]),
        ),
    ]
