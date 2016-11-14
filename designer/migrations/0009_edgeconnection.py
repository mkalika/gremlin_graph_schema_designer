# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-03 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0008_auto_20161003_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdgeConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to='designer.EdgeLabel')),
                ('fromVertex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_connections', to='designer.VertexLabel')),
                ('toVertex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_connections', to='designer.VertexLabel')),
            ],
        ),
    ]