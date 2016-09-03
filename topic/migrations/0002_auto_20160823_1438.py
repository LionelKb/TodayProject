# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-23 14:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtype',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=b'event_types/'),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='topic',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='core.Topic', verbose_name=b'Thematique'),
        ),
    ]