# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0019_member_help_first_time_wizard_current_step'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='help_first_time_wizard_current_step',
        ),
        migrations.AddField(
            model_name='member',
            name='help_first_time_wizard_cur_step',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
