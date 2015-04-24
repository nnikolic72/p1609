# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_member_smartfeed_last_seen_instagram_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='daily_new_friends_interactions',
            field=models.IntegerField(default=0, help_text='How many daily interactions a member had', null=True, verbose_name='Daily Interactions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='daily_new_friends_interactions_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
