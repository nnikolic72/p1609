# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_paymentlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='help_first_time_wizard_current_step',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
