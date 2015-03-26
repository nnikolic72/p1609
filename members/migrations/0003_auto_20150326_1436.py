# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='ig_api_limit_max',
            field=models.IntegerField(default=0, help_text='How many IG requests are available per period', null=True, verbose_name='IG API Limit Max', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='ig_api_limit_remaining',
            field=models.IntegerField(default=0, help_text='How many IG requests are remaining for period', null=True, verbose_name='IG API Limit Used', blank=True),
            preserve_default=True,
        ),
    ]
