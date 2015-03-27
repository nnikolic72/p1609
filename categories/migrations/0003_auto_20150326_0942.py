# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20150326_0929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryraw',
            options={'ordering': ('title',), 'verbose_name': 'Raw Category', 'verbose_name_plural': 'Raw Categories'},
        ),
        migrations.RemoveField(
            model_name='categoryraw',
            name='parent',
        ),
    ]
