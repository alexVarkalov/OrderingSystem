# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-19 06:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=30)),
                ('customer', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('paid_BYR', models.IntegerField(null=True)),
                ('paid_BYN', models.FloatField(null=True)),
                ('comment', models.CharField(max_length=300, null=True)),
                ('order_datetime', models.DateTimeField()),
            ],
        ),
    ]
