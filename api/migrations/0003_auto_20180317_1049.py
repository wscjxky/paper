# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-17 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180317_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='url',
            field=models.TextField(null=True, unique=True, verbose_name='链接de'),
        ),
    ]