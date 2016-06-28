# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-22 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('requestmedia', '0017_auto_20160621_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='id',
        ),
        migrations.AlterField(
            model_name='request',
            name='media_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='media_request', serialize=False, to='requestmedia.MediaItem'),
        ),
    ]