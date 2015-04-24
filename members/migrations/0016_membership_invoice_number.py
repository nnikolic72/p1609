# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_auto_20150417_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='invoice_number',
            field=models.CharField(default=b'', max_length=200, blank=True, help_text='Invoice number', null=True, verbose_name='Invoice number'),
            preserve_default=True,
        ),
    ]
