# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0024_auto_20150427_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membersmessage',
            name='show',
            field=models.BooleanField(default=True, help_text='Do we show message?', verbose_name='Show'),
            preserve_default=True,
        ),
    ]
