# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 02:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0013_profile_confirm_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='confirm_code',
            new_name='confirm_token',
        ),
    ]