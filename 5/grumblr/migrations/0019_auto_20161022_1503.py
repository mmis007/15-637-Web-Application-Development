# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-22 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0018_auto_20161022_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(default='', max_length=100),
        ),
    ]
