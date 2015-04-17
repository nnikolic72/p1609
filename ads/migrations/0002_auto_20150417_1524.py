# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='ad_id',
            field=models.CharField(help_text='Ad ID', max_length=50, null=True, verbose_name='Ad ID', blank=True),
            preserve_default=True,
        ),
    ]
