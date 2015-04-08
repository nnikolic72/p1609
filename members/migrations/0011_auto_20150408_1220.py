# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_auto_20150406_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='comments_in_last_minute_interval_start',
            field=models.DateTimeField(help_text='When comment limit period started', null=True, verbose_name='Comments period start', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='likes_in_last_minute_interval_start',
            field=models.DateTimeField(help_text='When like limit period started', null=True, verbose_name='Likes period start', blank=True),
            preserve_default=True,
        ),
    ]
