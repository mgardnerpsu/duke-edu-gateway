# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-03 00:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sequence', models.IntegerField(verbose_name='Display Sequence')),
                ('name', models.CharField(max_length=60, verbose_name='Choice Name')),
                ('label', models.TextField(verbose_name='Display Label (Answer)')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Correct Choice?')),
            ],
            options={
                'verbose_name': 'Field Choice',
                'db_table': 'choice',
                'ordering': ('field', 'sequence'),
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sequence', models.IntegerField(verbose_name='Display Sequence')),
                ('type', models.CharField(choices=[('multi-choice-radio', 'Multiple Choice - Single Answer (Radio Buttons)'), ('multi-choice-dropdown', 'Multiple Choice - Single Answer (Drop-down List)')], max_length=60, verbose_name='Type')),
                ('name', models.CharField(max_length=60, verbose_name='Field Name')),
                ('label', models.TextField(verbose_name='Display Label (Question)')),
            ],
            options={
                'verbose_name': 'Form Field',
                'db_table': 'field',
                'ordering': ('form', 'sequence'),
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('assessment', 'Assessment'), ('evaluation', 'Evaluation')], max_length=60, verbose_name='Type')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('descr', models.TextField(null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Form',
                'db_table': 'form',
            },
        ),
        migrations.AddField(
            model_name='field',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='forms.Form'),
        ),
        migrations.AddField(
            model_name='choice',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='forms.Field'),
        ),
    ]
