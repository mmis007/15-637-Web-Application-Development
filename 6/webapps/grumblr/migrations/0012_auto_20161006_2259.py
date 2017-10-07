# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 02:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0011_auto_20161006_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(related_name='follow_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='img'),
        ),
    ]
