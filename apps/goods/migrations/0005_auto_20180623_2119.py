# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-23 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20180623_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_front_image',
            field=models.ImageField(blank=True, null=True, upload_to='goods/images/', verbose_name='封面图'),
        ),
    ]
