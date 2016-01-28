# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=60, verbose_name='Label')),
                ('color', models.CharField(max_length=20, verbose_name='Hex Color for UX')),
            ],
            options={
                'verbose_name': 'Category',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('descr', models.TextField(verbose_name='Description')),
                ('learning_objective', models.TextField(verbose_name='Learning Objective')),
            ],
            options={
                'verbose_name': 'Course',
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='CourseAuthor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorcourses', to='authors.Author')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseauthors', to='content.Course', unique=True)),
            ],
            options={
                'verbose_name': 'Course Author',
                'db_table': 'course_author',
            },
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
                ('label', models.CharField(max_length=60, verbose_name='Label')),
                ('descr', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'CME Credit',
                'db_table': 'credit',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='authors',
            field=models.ManyToManyField(related_name='authors', through='content.CourseAuthor', to='authors.Author'),
        ),
    ]
