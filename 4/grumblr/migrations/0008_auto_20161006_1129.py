# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0007_auto_20161006_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(blank=True, default='', max_length=42),
        ),
    ]
