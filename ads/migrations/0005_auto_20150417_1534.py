# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_auto_20150417_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adinstance',
            name='page_id',
            field=models.CharField(help_text='Page ID', max_length=1000, null=True, verbose_name='Page ID', blank=True),
            preserve_default=True,
        ),
    ]
