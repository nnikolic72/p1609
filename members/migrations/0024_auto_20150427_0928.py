# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0023_membersmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membersmessage',
            name='text',
            field=models.CharField(help_text='Message Text', max_length=500, verbose_name='Message Text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membersmessage',
            name='title',
            field=models.CharField(help_text='Message Title', max_length=100, verbose_name='Message Title'),
            preserve_default=True,
        ),
    ]
