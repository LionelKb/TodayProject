# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 11:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(default=b'Paris', max_length=255, verbose_name='city_name')),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('image', models.ImageField(default=None, upload_to=b'events/')),
                ('price', models.PositiveSmallIntegerField(default=0)),
                ('address', models.CharField(default=b'non precis\xc3\xa9', max_length=150, verbose_name='address')),
                ('city', models.ForeignKey(default={b'city_name': b'Paris'}, on_delete=django.db.models.deletion.CASCADE, to='catho.City')),
                ('event_planner', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='organisateur')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50, verbose_name='label')),
                ('image', models.ImageField(default=None, upload_to=b'event_types/')),
            ],
            options={
                'verbose_name': 'event type',
                'verbose_name_plural': 'event types',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='note')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('object_id', models.PositiveIntegerField(verbose_name='object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type')),
            ],
            options={
                'verbose_name': 'note',
                'verbose_name_plural': 'notes',
            },
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('end_time', models.DateTimeField(verbose_name='end time')),
                ('is_multiple', models.BooleanField(default=False)),
                ('event', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='catho.Event', verbose_name='event')),
            ],
            options={
                'ordering': ('start_time', 'end_time'),
                'verbose_name': 'occurrence',
                'verbose_name_plural': 'occurrences',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catho.EventType', verbose_name='event type'),
        ),
    ]