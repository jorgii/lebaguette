# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requestmedia', '0004_auto_20160421_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvshowepisode',
            name='episode_imdbid',
            field=models.CharField(default='def', max_length=255, verbose_name='Episode IMDB ID'),
            preserve_default=False,
        ),
    ]
