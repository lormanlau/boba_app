# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-27 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track_boba', '0003_friendslist'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='lng',
            field=models.FloatField(null=True),
        ),
    ]
