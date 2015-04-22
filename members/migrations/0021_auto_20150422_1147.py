# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0020_auto_20150422_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='help_first_time_wizard_cur_step',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
