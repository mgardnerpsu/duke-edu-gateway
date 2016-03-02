# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-02 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20160131_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'course_category',
                'verbose_name': 'Course Category',
            },
        ),
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default='name', max_length=40, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursecategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Category'),
        ),
        migrations.AddField(
            model_name='coursecategory',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='categories',
            field=models.ManyToManyField(through='content.CourseCategory', to='content.Category'),
        ),
        migrations.AlterUniqueTogether(
            name='coursecategory',
            unique_together=set([('course', 'category')]),
        ),
    ]
