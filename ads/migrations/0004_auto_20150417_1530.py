# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_auto_20150417_1527'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ad',
            new_name='Advertisement',
        ),
        migrations.AlterModelOptions(
            name='adinstance',
            options={'ordering': ('advertisement',), 'get_latest_by': 'creation_date', 'verbose_name': 'Ad Instance', 'verbose_name_plural': 'Ad Instances'},
        ),
        migrations.RenameField(
            model_name='adinstance',
            old_name='ad',
            new_name='advertisement',
        ),
    ]
