# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(default=26),
            preserve_default=False,
        ),
    ]
