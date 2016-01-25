# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-25 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240, verbose_name='Title')),
                ('headline', models.TextField(verbose_name='Headline')),
                ('headline_thumbnail_url', models.CharField(max_length=240, verbose_name='Headline Portrait URL')),
                ('disclosure_summary', models.TextField(blank=True, null=True, verbose_name='Disclosure Summary')),
                ('disclosure_expires_on', models.DateTimeField(blank=True, null=True, verbose_name='Disclosure Expires On')),
            ],
            options={
                'verbose_name': 'Author',
                'db_table': 'author',
            },
        ),
    ]
