# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServerMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
