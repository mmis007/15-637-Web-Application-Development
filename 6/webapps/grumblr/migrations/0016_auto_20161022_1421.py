# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-22 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0015_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
