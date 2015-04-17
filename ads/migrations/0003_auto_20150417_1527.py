# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20150417_1524'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'ordering': ('ad_identification',), 'get_latest_by': 'creation_date', 'verbose_name': 'Ad', 'verbose_name_plural': 'Ads'},
        ),
        migrations.RenameField(
            model_name='ad',
            old_name='ad_id',
            new_name='ad_identification',
        ),
    ]
