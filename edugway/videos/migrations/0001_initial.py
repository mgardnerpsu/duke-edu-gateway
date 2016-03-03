# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-03 00:37
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('provider', models.CharField(choices=[('youtube', 'YouTube'), ('vimeo', 'Vimeo')], max_length=50, verbose_name='Provider')),
                ('provider_id', models.CharField(max_length=50, verbose_name='Provider ID')),
                ('provider_resource', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'verbose_name': 'Video',
                'db_table': 'video',
            },
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([('provider', 'provider_id')]),
        ),
    ]
