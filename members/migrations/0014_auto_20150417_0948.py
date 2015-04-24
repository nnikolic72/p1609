# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_auto_20150416_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='new_friends_in_last_day',
            field=models.IntegerField(default=0, help_text='How many new friends member interacted during last day', null=True, verbose_name='NewFriends in LD', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='new_friends_in_last_day_interval_start',
            field=models.DateTimeField(help_text='When new friends limit period started', null=True, verbose_name='NewFriends period start', blank=True),
            preserve_default=True,
        ),
    ]
