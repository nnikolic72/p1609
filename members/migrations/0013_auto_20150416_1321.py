# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_auto_20150416_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='help_reserved1',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_reserved2',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_reserved3',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_reserved4',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_reserved5',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
