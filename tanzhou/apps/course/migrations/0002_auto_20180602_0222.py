# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-02 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='describe',
            field=models.ImageField(null=True, upload_to='img/course/%Y/%m', verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='img/%Y/%m', verbose_name='封面图'),
        ),
    ]
