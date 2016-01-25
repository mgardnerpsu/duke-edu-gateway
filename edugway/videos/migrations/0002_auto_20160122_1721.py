# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-22 17:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='provider_resource_id',
            new_name='provider_id',
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([('provider', 'provider_id')]),
        ),
    ]
